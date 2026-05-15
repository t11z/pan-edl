#!/usr/bin/env python3
"""Auto-issue bot for pan-edl generator failures.

Triggered by the auto-issue workflow when the hourly update workflow
turns red. Reads the artifact uploaded by the hourly job (list of failed
slugs + their captured stderr), asks Claude for a diagnosis, then files
a GitHub issue per failure. If an open issue already covers a failure
the bot skips it to avoid spam — humans investigate, the bot just
surfaces problems.

Inputs (env):
  ANTHROPIC_API_KEY  required to call the Claude API
  GH_TOKEN           required for gh CLI auth (set by the workflow)
  GITHUB_REPOSITORY  owner/repo, set automatically by GH Actions

Inputs (argv):
  sys.argv[1]        path to the unpacked artifact directory
                     (defaults to /tmp/failures)

Behaviour flags (env):
  AUTO_ISSUE_DRY_RUN=1   don't actually call gh issue create/comment
  AUTO_ISSUE_MODEL       override model id (default claude-sonnet-4-6)
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import textwrap


REPO = os.environ.get('GITHUB_REPOSITORY', '')
DRY_RUN = os.environ.get('AUTO_ISSUE_DRY_RUN') == '1'
MODEL = os.environ.get('AUTO_ISSUE_MODEL', 'claude-sonnet-4-6')
ISSUE_LABEL = 'generator-failure'
TITLE_PREFIX = 'Generator failed:'


def gh(*args: str) -> str:
    """Run a gh CLI command and return stdout."""
    result = subprocess.run(
        ['gh', *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def diagnose_with_claude(slug: str, script_source: str, stderr_excerpt: str) -> dict:
    """Ask Claude for a structured diagnosis. Returns {"title", "body"}."""
    from anthropic import Anthropic

    client = Anthropic()
    user_prompt = textwrap.dedent(f"""\
        A scheduled run of a pan-edl generator script failed. Your task is
        to diagnose the failure and produce a concise GitHub issue title
        and body for maintainers.

        Generator slug: {slug}

        Script source (look at SOURCE_URL constants and the parse_* function):

        ```python
        {script_source}
        ```

        Captured stderr / error output:

        ```
        {stderr_excerpt[:4000]}
        ```

        Output a single JSON object with two fields:
        - "title": short title beginning with "{TITLE_PREFIX} {slug}".
        - "body": markdown issue body. Cover (1) the most plausible root
          cause — page structure change vs network outage vs validation
          regression; (2) what to check first (anchor selectors,
          ALLOW_SUFFIXES, SOURCE_URL response); (3) one suggested next
          step. Include the captured error verbatim in a fenced code
          block. Keep the body under 250 words.

        Output ONLY the JSON object — no prose, no markdown fences around it.
        """)

    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": user_prompt}],
    )
    text = ''.join(block.text for block in response.content if hasattr(block, 'text')).strip()
    # Tolerate the model wrapping the JSON in code fences.
    if text.startswith('```'):
        text = text.strip('`')
        if text.lower().startswith('json'):
            text = text[4:]
        text = text.strip()
    return json.loads(text)


def open_issue_for_slug(slug: str) -> int | None:
    """Return number of an open issue whose title starts with the slug marker."""
    title_marker = f"{TITLE_PREFIX} {slug}"
    out = gh(
        'issue', 'list',
        '--repo', REPO,
        '--state', 'open',
        '--label', ISSUE_LABEL,
        '--json', 'number,title',
        '--limit', '100',
    )
    for issue in json.loads(out):
        if issue['title'].startswith(title_marker):
            return issue['number']
    return None


def create_issue(title: str, body: str) -> None:
    if DRY_RUN:
        print(f"[dry-run] would create issue: {title!r}")
        return
    gh(
        'issue', 'create',
        '--repo', REPO,
        '--title', title,
        '--body', body,
        '--label', ISSUE_LABEL,
    )


def fallback_issue(slug: str, stderr_excerpt: str) -> dict:
    """Build a minimal title/body when Claude is unavailable."""
    return {
        'title': f"{TITLE_PREFIX} {slug}",
        'body': (
            f"Automated diagnosis was unavailable; raw error follows.\n\n"
            f"```\n{stderr_excerpt[:3500]}\n```"
        ),
    }


def process_failure(slug: str, repo_root: pathlib.Path, logs_dir: pathlib.Path) -> None:
    script = repo_root / slug / f"{slug}.py"
    if not script.exists():
        print(f"[{slug}] script not found at {script}, skipping")
        return

    err_file = logs_dir / f"{slug}.err"
    stderr_excerpt = err_file.read_text() if err_file.exists() else "(no stderr captured)"

    if open_issue_for_slug(slug) is not None:
        print(f"[{slug}] open issue already exists; skipping (humans investigate, bot does not spam)")
        return

    script_source = script.read_text()
    try:
        diagnosis = diagnose_with_claude(slug, script_source, stderr_excerpt)
        title, body = diagnosis['title'], diagnosis['body']
    except Exception as exc:
        print(f"[{slug}] diagnosis failed ({exc}); falling back to minimal issue")
        fallback = fallback_issue(slug, stderr_excerpt)
        title, body = fallback['title'], fallback['body']

    if not title.startswith(TITLE_PREFIX):
        title = f"{TITLE_PREFIX} {slug} — {title}"

    body += (
        f"\n\n---\n_Filed by `.github/scripts/auto_issue_bot.py` "
        f"for slug `{slug}`. Closes automatically only via human review._"
    )
    create_issue(title, body)
    print(f"[{slug}] issue filed.")


def main(artifact_dir: str) -> int:
    artifact = pathlib.Path(artifact_dir)
    slugs_file = artifact / 'failed_generators.txt'
    logs_dir = artifact / 'generator-logs'
    repo_root = pathlib.Path(__file__).resolve().parents[2]

    if not slugs_file.exists() or slugs_file.stat().st_size == 0:
        print("No failed generators reported; nothing to do.")
        return 0

    failed = [s.strip() for s in slugs_file.read_text().splitlines() if s.strip()]
    print(f"Processing {len(failed)} failed generator(s): {', '.join(failed)}")
    for slug in failed:
        try:
            process_failure(slug, repo_root, logs_dir)
        except Exception as exc:
            print(f"[{slug}] unexpected error while filing issue: {exc}")

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '/tmp/failures'))
