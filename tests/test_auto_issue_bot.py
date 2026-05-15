"""Tests for the auto-issue bot script.

These tests stub out gh CLI subprocess calls and the Anthropic SDK so the
bot's logic can be exercised without network access or secrets.
"""
import importlib.util
import json
import pathlib
import sys
from types import SimpleNamespace

import pytest


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


def _load_bot():
    spec = importlib.util.spec_from_file_location(
        'auto_issue_bot',
        REPO_ROOT / '.github' / 'scripts' / 'auto_issue_bot.py',
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bot = _load_bot()


@pytest.fixture
def artifact_dir(tmp_path: pathlib.Path) -> pathlib.Path:
    (tmp_path / 'failed_generators.txt').write_text('demo-slug\n')
    logs = tmp_path / 'generator-logs'
    logs.mkdir()
    (logs / 'demo-slug.err').write_text(
        "Traceback (most recent call last):\n"
        "  File \"demo-slug/demo-slug.py\", line 12, in <module>\n"
        "lib.scraping.PageStructureError: none of the expected anchor selectors found: ['main', 'article']\n"
    )
    return tmp_path


@pytest.fixture
def repo_with_script(tmp_path: pathlib.Path, monkeypatch) -> pathlib.Path:
    """Pretend the repo root contains a generator script."""
    repo = tmp_path / 'repo'
    repo.mkdir()
    slug_dir = repo / 'demo-slug'
    slug_dir.mkdir()
    (slug_dir / 'demo-slug.py').write_text(
        '"""docstring"""\n'
        'SOURCE_URL = "https://vendor.example/docs"\n'
        'def parse_demo_page(html): return []\n'
    )
    # Point the bot at this repo root by patching the resolve(parents[2]) line.
    monkeypatch.setattr(bot, '__file__', str(repo / '.github' / 'scripts' / 'auto_issue_bot.py'))
    return repo


class TestFallbackIssue:
    def test_has_required_fields(self):
        result = bot.fallback_issue('foo', 'oh no')
        assert result['title'].startswith(bot.TITLE_PREFIX)
        assert 'foo' in result['title']
        assert 'oh no' in result['body']
        assert '```' in result['body']

    def test_truncates_long_stderr(self):
        huge = 'x' * 10_000
        result = bot.fallback_issue('foo', huge)
        assert len(result['body']) < 6000


class TestOpenIssueLookup:
    def test_returns_matching_issue_number(self, monkeypatch):
        sample = json.dumps([
            {'number': 42, 'title': 'Generator failed: demo-slug — page structure changed'},
            {'number': 7, 'title': 'Generator failed: other-slug — broken'},
        ])
        monkeypatch.setattr(bot, 'gh', lambda *a: sample)
        assert bot.open_issue_for_slug('demo-slug') == 42

    def test_returns_none_when_no_match(self, monkeypatch):
        monkeypatch.setattr(bot, 'gh', lambda *a: json.dumps([
            {'number': 99, 'title': 'Generator failed: other-slug — broken'},
        ]))
        assert bot.open_issue_for_slug('demo-slug') is None

    def test_returns_none_on_empty_list(self, monkeypatch):
        monkeypatch.setattr(bot, 'gh', lambda *a: '[]')
        assert bot.open_issue_for_slug('demo-slug') is None


class TestProcessFailure:
    def test_skips_when_open_issue_exists(self, monkeypatch, artifact_dir, repo_with_script, capsys):
        monkeypatch.setattr(bot, 'open_issue_for_slug', lambda slug: 42)
        called = []
        monkeypatch.setattr(bot, 'create_issue', lambda title, body: called.append((title, body)))

        bot.process_failure('demo-slug', repo_with_script, artifact_dir / 'generator-logs')

        assert called == []
        assert 'open issue already exists' in capsys.readouterr().out

    def test_creates_issue_when_none_exists(self, monkeypatch, artifact_dir, repo_with_script):
        monkeypatch.setattr(bot, 'open_issue_for_slug', lambda slug: None)
        called = []
        monkeypatch.setattr(bot, 'create_issue', lambda title, body: called.append((title, body)))

        def fake_diagnose(slug, script_source, stderr_excerpt):
            assert slug == 'demo-slug'
            assert 'SOURCE_URL' in script_source
            assert 'PageStructureError' in stderr_excerpt
            return {
                'title': 'Generator failed: demo-slug — anchor selectors no longer match',
                'body': 'Likely cause: vendor renamed the article container.',
            }
        monkeypatch.setattr(bot, 'diagnose_with_claude', fake_diagnose)

        bot.process_failure('demo-slug', repo_with_script, artifact_dir / 'generator-logs')

        assert len(called) == 1
        title, body = called[0]
        assert title.startswith('Generator failed: demo-slug')
        assert 'anchor selectors' in title
        assert 'auto_issue_bot.py' in body  # signature footer

    def test_falls_back_when_claude_errors(self, monkeypatch, artifact_dir, repo_with_script):
        monkeypatch.setattr(bot, 'open_issue_for_slug', lambda slug: None)
        called = []
        monkeypatch.setattr(bot, 'create_issue', lambda title, body: called.append((title, body)))

        def fake_diagnose(*a, **k):
            raise RuntimeError("API down")
        monkeypatch.setattr(bot, 'diagnose_with_claude', fake_diagnose)

        bot.process_failure('demo-slug', repo_with_script, artifact_dir / 'generator-logs')

        assert len(called) == 1
        title, body = called[0]
        assert title == 'Generator failed: demo-slug'
        assert 'PageStructureError' in body
        assert '```' in body

    def test_skips_when_script_missing(self, monkeypatch, artifact_dir, repo_with_script, capsys):
        called = []
        monkeypatch.setattr(bot, 'create_issue', lambda title, body: called.append((title, body)))
        monkeypatch.setattr(bot, 'open_issue_for_slug', lambda slug: None)

        bot.process_failure('nonexistent-slug', repo_with_script, artifact_dir / 'generator-logs')

        assert called == []
        assert 'script not found' in capsys.readouterr().out


class TestMain:
    def test_no_artifact_returns_zero(self, tmp_path, capsys):
        # No failed_generators.txt at all
        assert bot.main(str(tmp_path)) == 0
        assert 'nothing to do' in capsys.readouterr().out.lower()

    def test_empty_artifact_returns_zero(self, tmp_path, capsys):
        (tmp_path / 'failed_generators.txt').write_text('')
        assert bot.main(str(tmp_path)) == 0
        assert 'nothing to do' in capsys.readouterr().out.lower()
