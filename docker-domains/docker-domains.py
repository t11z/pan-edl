#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

url = 'https://docs.docker.com/desktop/allow-list/'

try:
    response = requests.get(url)
    response.raise_for_status()
except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as err:
    print(f"An error occurred while trying to fetch data: {err}")
else:
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
                
        unique_domains = list(set(domains))
        unique_domains.sort()
 
        if unique_domains:
            with open('docker-domains/docker-domains.txt', 'w') as file:
                for domain in unique_domains:
                    file.write(domain + '/\n')
    except AttributeError as e:
        print(f"An error occurred while parsing the HTML: {e}")
