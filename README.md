# Palo Alto Networks External Dynamic Lists
[![Hourly update](https://github.com/t11z/pan-edl/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/t11z/pan-edl/actions/workflows/main.yml)

External Dynamic Lists that can be consumed by Palo Alto Networks firewalls

## How to add it to your Palo Alto Networks firewall

1. Download GitHub Intermediate- and Root CA certificates 
2. Import certificates into your firewall (Device -> Certificate Management -> Certificates -> Import)
3. Create Certificate Profile in your firewall (Device -> Certificate Management -> Certificate Profile)
4. Choose a name and add intermediate and root CA certificates to the Certificate Profile
5. Add External Dynamic List object according to your needs (Objects -> External Dynamic Lists -> Add) and select the Certificate Profile you have just created
6. Choose an EDL from the list below, add it to the input box and click on "OK"
7. Commit your configuration

**Important**: The firewall will only download the list, if you use it in your rulebase. If the list is not used in the rulebase, it is expected behavior that the list remains empty.

Each list's Status badge shows the result of the most recent hourly run plus the current entry count (refreshed by [shields.io](https://shields.io/badges/endpoint-badge) from `.badges/<slug>.json`). A red `failing` badge means the last generator run errored — the published `.txt` is still the previous known-good content (the `write_edl` safety net never truncates), it just isn't being refreshed.

| List name | Description | EDL Type | EDL URL | Status |
| --- | --- | --- | --- | --- |
| Debian Mirrors | List of all official Debian repository mirrors | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/debian-mirrors/debian-mirrors.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/debian-mirrors.json) |
| Ubuntu Mirrors | List of all official Ubuntu repository mirrors | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/ubuntu-mirrors/ubuntu-mirrors.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/ubuntu-mirrors.json) |
| Docker URLs | List of all URLs used in Docker Engine and Docker Desktop | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/docker-domains/docker-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/docker-domains.json) |
| PyPI Domains | Endpoints for installing Python packages via pip | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/pypi-domains/pypi-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/pypi-domains.json) |
| npm Domains | Endpoints for the npm registry and CLI | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/npm-domains/npm-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/npm-domains.json) |
| Maven Central Domains | Endpoints for Maven Central (Apache Maven / Sonatype) | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/maven-central-domains/maven-central-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/maven-central-domains.json) |
| NuGet Domains | Endpoints for the NuGet package registry | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/nuget-domains/nuget-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/nuget-domains.json) |
| crates.io Domains | Endpoints for the Rust crates.io registry | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/crates-io-domains/crates-io-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/crates-io-domains.json) |
| Go Proxy Domains | Endpoints for the official Go module proxy and checksum DB | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/go-proxy-domains/go-proxy-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/go-proxy-domains.json) |
| RubyGems Domains | Endpoints for the RubyGems registry | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/rubygems-domains/rubygems-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/rubygems-domains.json) |
| Tor Exit Nodes | Exit-relay IPs from the Tor Project bulk exit list (deny use case) | IP List | https://raw.githubusercontent.com/t11z/pan-edl/main/tor-exit-nodes/tor-exit-nodes.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/tor-exit-nodes.json) |
| Tor Relays | All running Tor relay IPs from the Tor Project Onionoo API | IP List | https://raw.githubusercontent.com/t11z/pan-edl/main/tor-relays/tor-relays.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/tor-relays.json) |
| Quay.io Domains | Endpoints for the Quay.io container registry (Red Hat) | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/quay-io-domains/quay-io-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/quay-io-domains.json) |
| GHCR Domains | Endpoints for the GitHub Container Registry | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/ghcr-domains/ghcr-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/ghcr-domains.json) |
| GCR Domains | Endpoints for Google Container Registry and Artifact Registry | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/gcr-domains/gcr-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/gcr-domains.json) |
| MCR Domains | Endpoints for Microsoft Container Registry | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/mcr-microsoft-domains/mcr-microsoft-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/mcr-microsoft-domains.json) |
| Red Hat Registry Domains | Endpoints for the Red Hat container registries | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/redhat-registry-domains/redhat-registry-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/redhat-registry-domains.json) |
| Rocky Linux Mirrors | List of official Rocky Linux repository mirrors | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/rocky-linux-mirrors/rocky-linux-mirrors.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/rocky-linux-mirrors.json) |
| AlmaLinux Mirrors | List of official AlmaLinux repository mirrors | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/almalinux-mirrors/almalinux-mirrors.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/almalinux-mirrors.json) |
| Fedora Mirrors | List of official Fedora repository mirrors | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/fedora-mirrors/fedora-mirrors.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/fedora-mirrors.json) |
| openSUSE Mirrors | List of official openSUSE repository mirrors | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/opensuse-mirrors/opensuse-mirrors.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/opensuse-mirrors.json) |
| Alpine Linux Mirrors | List of official Alpine Linux repository mirrors | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/alpine-mirrors/alpine-mirrors.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/alpine-mirrors.json) |
| Arch Linux Mirrors | List of official Arch Linux repository mirrors | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/arch-mirrors/arch-mirrors.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/arch-mirrors.json) |
| Kali Linux Mirrors | List of official Kali Linux repository mirrors | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/kali-mirrors/kali-mirrors.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/kali-mirrors.json) |
| JetBrains Domains | Endpoints required by JetBrains IDEs (firewall allow-list) | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/jetbrains-domains/jetbrains-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/jetbrains-domains.json) |
| VS Code Domains | Endpoints required by Visual Studio Code | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/vscode-domains/vscode-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/vscode-domains.json) |
| Azul Domains | Endpoints for Azul Zulu / Platform JDK downloads | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/azul-domains/azul-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/azul-domains.json) |
| Adoptium Domains | Endpoints for Eclipse Adoptium (Temurin) JDK | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/adoptium-domains/adoptium-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/adoptium-domains.json) |
| Corretto Domains | Endpoints for Amazon Corretto JDK | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/corretto-domains/corretto-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/corretto-domains.json) |
| Mozilla Update Domains | Endpoints for Firefox / Thunderbird updates and services | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/mozilla-update-domains/mozilla-update-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/mozilla-update-domains.json) |
| Chrome Update Domains | Endpoints for Google Chrome updates and Chrome Enterprise | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/chrome-update-domains/chrome-update-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/chrome-update-domains.json) |
| Edge Update Domains | Endpoints for Microsoft Edge updates and services | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/edge-update-domains/edge-update-domains.txt | ![Status](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/t11z/pan-edl/main/.badges/edge-update-domains.json) |

## Contributing a new list

Each EDL has its own directory at the repo root, containing a generator script and the produced `.txt` file. The hourly GitHub Actions workflow auto-discovers every `*/<dir>.py` script under the repo root, so adding a new list means: create a directory, drop in a generator, list it in the table above.

A generator must:

1. Source data only from vendor-native or authoritative public infrastructure (vendor docs/APIs, Certificate Transparency logs, RIR databases, DNS). Third-party aggregators and community-maintained lists are not accepted.
2. Use `lib.edl_utils.write_edl(entries, path, EDLType.<TYPE>)` to produce the output. Validation against PAN-OS EDL formatting rules happens there.
3. Live at `<slug>/<slug>.py` and write to `<slug>/<slug>.txt`.
4. Add a row to the table above, including a Status badge that points at `.badges/<slug>.json`. The hourly workflow writes that file automatically — no need to commit it by hand.

Run locally with `PYTHONPATH=. python <slug>/<slug>.py`. Validator tests: `python -m pytest tests/`.

## Auto-issue bot

The `.github/workflows/auto-issue.yml` workflow runs after every hourly update. When the update workflow turns red — for example because a vendor's documentation page changed structure and a scraper can no longer find its anchor — the bot:

1. Downloads the per-generator stderr artifact uploaded by the hourly job.
2. Invokes the official [Claude Code GitHub Action](https://github.com/anthropics/claude-code-action) with a natural-language brief. Claude reads each failed generator's source code and captured error, diagnoses the root cause, and files an issue via `gh` CLI from inside the action.
3. Issues are tagged `generator-failure`. If an open issue for the same slug already exists, the bot stays silent — humans investigate, the bot doesn't spam.

This means the published `raw.githubusercontent.com/.../<slug>/<slug>.txt` URLs keep serving the last known-good list (the `write_edl` safety net refuses to truncate on empty parser output), while maintainers get a structured, actionable issue with proposed next steps within an hour of a regression.

Required repo secret: **`CLAUDE_CODE_OAUTH_TOKEN`** (generate with `claude code setup-token` and add it under Settings → Secrets and variables → Actions). The hourly update workflow itself has no Claude dependency.
