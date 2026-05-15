# Rollout Report

Status per EDL list considered for inclusion in the pan-edl repository.

Legend:
- ✅ merged — generator implemented, validates against PAN-OS rules, published as EDL
- ❌ dropped — no vendor-native machine-readable source available, or validation failed
- 🟡 pending — planned in a future batch

## Batch A — Package managers & Tor

| Slug | Status | Source | EDL Type | Size | Notes |
| --- | --- | --- | --- | --- | --- |
| `pypi-domains` | ✅ merged | PyPI/PSF docs (pypi.org/help, packaging.python.org) | URL List | 4 entries | Static, vendor-cited |
| `npm-domains` | ✅ merged | docs.npmjs.com, npm/cli repo | URL List | 4 entries | Static, vendor-cited |
| `maven-central-domains` | ✅ merged | central.sonatype.org, maven.apache.org/repository | URL List | 6 entries | Static, vendor-cited |
| `nuget-domains` | ✅ merged | learn.microsoft.com/nuget, NuGet v3 service index | URL List | 4 entries | Static, vendor-cited |
| `crates-io-domains` | ✅ merged | doc.rust-lang.org/cargo (registries reference) | URL List | 3 entries | Static, vendor-cited |
| `go-proxy-domains` | ✅ merged | go.dev/ref/mod (env var reference) | URL List | 5 entries | Static, vendor-cited |
| `rubygems-domains` | ✅ merged | guides.rubygems.org (API guide) | URL List | 3 entries | Static, vendor-cited |
| `tor-exit-nodes` | ✅ merged | check.torproject.org/exit-addresses | IP List | dynamic | Hourly refresh, deny use case |
| `tor-relays` | ✅ merged | onionoo.torproject.org/details (Tor's own API) | IP List | dynamic | Hourly refresh |

### Notes on source-of-truth policy

The package-manager lists are intentionally curated static lists (with vendor-doc
citations in each generator header) rather than scraped pages. The reason: none of
these vendors publishes a single canonical "firewall allow-list" page in a
machine-readable form. Curating the list ourselves — sourcing only from the
vendor's own documentation — makes pan-edl the source-of-truth, which is
exactly the project goal. Git history serves as the change log; a vendor adding
or removing a host is reflected via a PR to the generator script.

The Tor lists are dynamic because the Tor Project publishes the data
machine-readably (bulk exit list + Onionoo JSON API).

## Batch B — Container registries

| Slug | Status | Source | EDL Type | Size | Notes |
| --- | --- | --- | --- | --- | --- |
| `quay-io-domains` | ✅ merged | docs.quay.io, access.redhat.com/articles/2477561 | URL List | 6 entries | Static, vendor-cited |
| `ghcr-domains` | ✅ merged | docs.github.com (container registry docs) | URL List | 4 entries | Static, vendor-cited |
| `gcr-domains` | ✅ merged | cloud.google.com/container-registry, /artifact-registry | URL List | 9 entries | Static, includes Artifact Registry |
| `mcr-microsoft-domains` | ✅ merged | learn.microsoft.com (azure/container-registry firewall doc) | URL List | 2 entries | Static, vendor-cited |
| `redhat-registry-domains` | ✅ merged | access.redhat.com/RegistryAuthentication, /articles/2208611 | URL List | 7 entries | Static, vendor-cited |

## Batch C — Linux distro mirrors

All dynamic — each generator scrapes the distro project's own mirror list
endpoint and writes a fresh `.txt` every hour.

| Slug | Status | Source | EDL Type | Notes |
| --- | --- | --- | --- | --- |
| `arch-mirrors` | ✅ merged | archlinux.org/mirrors/status/json/ | URL List | JSON API (machine-readable) |
| `alpine-mirrors` | ✅ merged | mirrors.alpinelinux.org/MIRRORS.txt | URL List | Plain text |
| `kali-mirrors` | ✅ merged | http.kali.org/README.mirrorlist | URL List | Plain text |
| `rocky-linux-mirrors` | ✅ merged | mirrors.rockylinux.org/mirrormanager/mirrors | URL List | HTML scrape |
| `almalinux-mirrors` | ✅ merged | mirrors.almalinux.org/ | URL List | HTML scrape |
| `fedora-mirrors` | ✅ merged | mirrors.fedoraproject.org/publiclist/ | URL List | HTML scrape, follows release subpages |
| `opensuse-mirrors` | ✅ merged | mirrors.opensuse.org/list/all.html | URL List | HTML scrape |

## Batch D — JDK / dev tools

All dynamic scrapers using `lib/scraping.py` (anchor-based parsing with
vendor-domain allow-list filter). On vendor page structure change the
generator fails loudly and the existing `.txt` is preserved.

| Slug | Status | Source | EDL Type | Notes |
| --- | --- | --- | --- | --- |
| `jetbrains-domains` | ✅ merged | intellij-support.jetbrains.com/.../360001214939 | URL List | Official JetBrains firewall allow-list article |
| `vscode-domains` | ✅ merged | code.visualstudio.com/docs/setup/network | URL List | Microsoft network-config docs |
| `azul-domains` | ✅ merged | docs.azul.com/core/getting-started | URL List | Azul Zulu install docs |
| `adoptium-domains` | ✅ merged | adoptium.net/installation/ | URL List | Eclipse Adoptium install docs |
| `corretto-domains` | ✅ merged | docs.aws.amazon.com/corretto/.../downloads-list.html | URL List | AWS Corretto downloads list |

## Batch E — Browser / update CDNs

| Slug | Status | Source | EDL Type | Notes |
| --- | --- | --- | --- | --- |
| `mozilla-update-domains` | ✅ merged | support.mozilla.org/.../configure-firewalls-... | URL List | Official Firefox firewall KB |
| `chrome-update-domains` | ✅ merged | support.google.com/chrome/a/answer/6350036 | URL List | Chrome Enterprise admin help |
| `edge-update-domains` | ✅ merged | learn.microsoft.com/deployedge/microsoft-edge-security-endpoints | URL List | Microsoft Edge security endpoints |

## Library improvements (this batch)

- `write_edl` now refuses to write fewer than `min_entries` (default 1).
  When a parser produces an empty result the last known-good `.txt` is
  preserved on disk. This guarantees published EDL URLs never serve an
  empty file even when a vendor page changes structure.
- New `lib/scraping.py` with defensive helpers: anchor selectors with
  fallbacks, hostname-token extraction from DOM subtrees, and an
  allow-suffix filter to reject unrelated example hostnames.
- Workflow split: individual generator failures no longer block commits
  from successful generators; the workflow turns red only after all
  successful changes have been pushed. Each failed generator is
  reported in the workflow log.

## Pending batches

| Batch | Slug | Status | Notes |
| --- | --- | --- | --- |
| F | AnyDesk (CT-logs + DNS) | 🟡 pending | |
| Retrofit | Batch A + B static lists → dynamic scrapers | 🟡 pending | Track separately |
