#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

url = 'https://launchpad.net/ubuntu/+archivemirrors'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', attrs={'id': 'mirrors_list'})

domains = []

for table in tables:
    links = table.find_all('a')
    for link in links:
        href = link.get('href')
        if href:
            domain = urlparse(href).netloc
            domains.append(domain)

unique_domains = list(set(domains))
with open('ubuntu-mirrors/ubuntu-mirrors.txt', 'w') as file:
    for domain in unique_domains:
        file.write(domain + '/\n')
