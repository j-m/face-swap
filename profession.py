import requests
from bs4 import BeautifulSoup

name = 'anthony joshua'
name = (name.split())
search = 'https://www.google.co.uk/search?q='
for word in name:
    search += word+'+'

print(search[:-1])
result = requests.get(search[:-1])

if result.status_code == requests.codes.ok:
    soup = BeautifulSoup(result.content,'lxml')
    print(len(soup))

    profession = soup.find_all("div", class_="_zdb _Pxg")
    print(profession[0].text)
