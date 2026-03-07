#!/usr/bin/env python3.12
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
sys.path.insert(0, '.')
from lib.edl_utils import write_edl

url = 'https://docs.docker.com/desktop/allow-list/'

try:
    response = requests.get(url, headers={'User-Agent': 'pan-edl/1.0 (github.com/t11z/pan-edl)'})
    response.raise_for_status()
except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as err:
    print(f"An error occurred while trying to fetch data: {err}")
    sys.exit(1)

try:
    soup = BeautifulSoup(response.text, 'html.parser')
    h2 = soup.find('h2', attrs={'id': 'domain-urls-to-allow'})
    div = h2.find_next('div', class_='overflow-x-auto')

    domains = []
    domains.append("download.docker.com")

    if div:
        table = div.find('table')
        if table:
            links = table.find_all('a')
            for link in links:
                href = link.get('href')
                if href:
                    domain = urlparse(href).netloc
                    domains.append(domain)

    write_edl(domains, 'docker-domains/docker-domains.txt')
except AttributeError as e:
    print(f"An error occurred while parsing the HTML: {e}")
    sys.exit(1)
