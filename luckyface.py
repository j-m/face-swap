# luckyface.py - Will go through google images until it finds a valid face.

# TRY EXCEPT IN GET PORTRAIT
# _gdf kno-fb-ctx

import os
import requests
import shutil
import wikipedia
from bs4 import BeautifulSoup

import faceswap


def search(person):
    try:
        wikipedia.page(person)
        return wikipedia.page(person)
    except wikipedia.exceptions.PageError:
        print(person, 'not found.')
    if len(wikipedia.search(person)) > 0:
        print('Assuming you meant', wikipedia.search('napoleona')[0])
        return wikipedia.page(wikipedia.search('napoleona')[0])
    print('Nobody found...')


def get_portrait(wikipage):
    result = requests.get('http://en.wikipedia.org/wiki/' + wikipage.title)
    # All images in infobox
    if result.status_code == requests.codes.ok:
        soup = BeautifulSoup(result.content, 'lxml')
        images = soup.select('table.infobox a.image img[src]')
        portrait_link = images[0]['src']
        return 'https:' + portrait_link
    else:
        return get_portrait(wikipage)


def save_portrait(person):
    # save to local/relative directory/path.
    person_page = search(person)
    person_portrait = get_portrait(person_page)
    file_name = person_portrait.rsplit('/', 1)[-1]

    response = requests.get(person_portrait, stream=True)
    with open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

    return [person_page.title, file_name]


def all_images(wiki_search):
    return search(wiki_search).images


def get_parents(father, mother):
    parents = [save_portrait(father), save_portrait(mother)]
    return parents


def make_baby(father, mother):
    parents = get_parents(father, mother)
    if os.path.isfile(parents[0][1]) and os.path.isfile(parents[1][1]):
        print(parents[0][0], '&', parents[1][0], 'are having a baby!')
        faceswap.birth(parents[0][1], parents[1][1])
    else:
        print('parents don\'t exist')


if __name__ == '__main__':
    parent1 = 'Adelle'
    parent2 = 'Phil Mitchell'
    try:
        make_baby(parent1, parent2)
    except:
        print('Error')
