#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

url = 'https://launchpad.net/ubuntu/+archivemirrors'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# Find all <table> elements
tables = soup.find_all('table', attrs={'id': 'mirrors_list'})

# Initialize a list to store the domains
domains = []

# Iterate over each <table>
for table in tables:
    # Find all <a> tags within the table
    links = table.find_all('a')
    # Extract the href attribute and parse the domain
    for link in links:
        href = link.get('href')
        if href:
            domain = urlparse(href).netloc
            domains.append(domain)

# Remove duplicates and print the list of domains
unique_domains = list(set(domains))
with open('debian-mirrors.txt', 'w') as file:
    for domain in unique_domains:
        file.write(domain + '/\n')
