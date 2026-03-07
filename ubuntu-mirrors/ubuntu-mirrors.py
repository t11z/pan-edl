#!/usr/bin/env python3.12
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
sys.path.insert(0, '.')
from lib.edl_utils import write_edl

url = 'https://launchpad.net/ubuntu/+archivemirrors'

try:
    response = requests.get(url, headers={'User-Agent': 'pan-edl/1.0 (github.com/t11z/pan-edl)'})
    response.raise_for_status()
except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as err:
    print(f"An error occurred while trying to fetch data: {err}")
    sys.exit(1)

try:
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table', attrs={'id': 'mirrors_list'})

    domains = []
    domains.append("archive.ubuntu.com")
    domains.append("*.archive.ubuntu.com")
    domains.append("security.ubuntu.com")

    for table in tables:
        links = table.find_all('a')
        for link in links:
            href = link.get('href')
            if href:
                domain = urlparse(href).netloc
                if domain:
                    domains.append(domain)

    write_edl(domains, 'ubuntu-mirrors/ubuntu-mirrors.txt')
except Exception as err:
    print(f"An error occurred while parsing the data: {err}")
    sys.exit(1)
