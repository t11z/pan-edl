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

## Pending batches

| Batch | Slug | Status | Notes |
| --- | --- | --- | --- |
| C | Linux distros (rocky, alma, fedora, opensuse, alpine, arch, kali) | 🟡 pending | |
| D | JDK / dev tools (adoptium, azul, corretto, jetbrains, vscode) | 🟡 pending | |
| E | Browser/update CDNs (mozilla, chrome, edge) | 🟡 pending | |
| F | AnyDesk (CT-logs + DNS) | 🟡 pending | |
