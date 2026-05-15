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

| List name | Description | EDL Type | EDL URL |
| --- | --- | --- | --- |
| Debian Mirrors | List of all official Debian repository mirrors | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/debian-mirrors/debian-mirrors.txt |
| Ubuntu Mirrors | List of all official Ubuntu repository mirrors | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/ubuntu-mirrors/ubuntu-mirrors.txt |
| Docker URLs | List of all URLs used in Docker Engine and Docker Desktop | URL List | https://raw.githubusercontent.com/t11z/pan-edl/main/docker-domains/docker-domains.txt |

## Contributing a new list

Each EDL has its own directory at the repo root, containing a generator script and the produced `.txt` file. The hourly GitHub Actions workflow auto-discovers every `*/<dir>.py` script under the repo root, so adding a new list means: create a directory, drop in a generator, list it in the table above.

A generator must:

1. Source data only from vendor-native or authoritative public infrastructure (vendor docs/APIs, Certificate Transparency logs, RIR databases, DNS). Third-party aggregators and community-maintained lists are not accepted.
2. Use `lib.edl_utils.write_edl(entries, path, EDLType.<TYPE>)` to produce the output. Validation against PAN-OS EDL formatting rules happens there.
3. Live at `<slug>/<slug>.py` and write to `<slug>/<slug>.txt`.

Run locally with `PYTHONPATH=. python <slug>/<slug>.py`. Validator tests: `python -m pytest tests/`.
