import requests
from bs4 import BeautifulSoup

response = requests.get(input("url\n> "))
response.raise_for_status()

print(response.text)

soup = BeautifulSoup(response.text, 'html.parser')

print(soup.prettify())
print(soup.find_all('img'))