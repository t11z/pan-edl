#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

url = 'https://launchpad.net/ubuntu/+archivemirrors'

try:
    response = requests.get(url)
    response.raise_for_status()
except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as err:
    print(f"An error occurred while trying to fetch data: {err}")
else:
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

        unique_domains = list(set(domains))
        unique_domains.sort()

        if unique_domains:
            with open('ubuntu-mirrors/ubuntu-mirrors.txt', 'w') as file:
                for domain in unique_domains:
                    file.write(domain + '/\n')
    except Exception as err:
        print(f"An error occurred while parsing the data: {err}")
