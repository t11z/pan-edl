def write_edl(domains: list[str], filepath: str) -> None:
    unique_domains = sorted(set(domains))
    with open(filepath, 'w') as f:
        for domain in unique_domains:
            f.write(domain + '/\n')
