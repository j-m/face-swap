import requests
from bs4 import BeautifulSoup
#_gdf kno-fb-ctx
name = 'anthony joshua'
name = (name.split())
search = 'https://www.google.co.uk/search?q='
for word in name:
    search += word+'+'

print(search[:-1])
result = requests.get(search[:-1])

if result.status_code == requests.codes.ok:
    soup = BeautifulSoup(result.content,'lxml')
soup = BeautifulSoup(result.text, 'lxml')
print(len(soup))

proffession = soup.find_all("div", class_="_zdb _Pxg")
print(proffession[0].text)
