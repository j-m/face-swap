#! python3
# luckyface.py - Will go through google images until it finds a valid face.

#TRY EXCEPT IN GET PORTRAIT
#_gdf kno-fb-ctx

import sys, wikipedia, shutil, requests, time, os
from bs4 import BeautifulSoup
import faceswap


def search(person):
    try:
        wikipedia.page(person)
        return wikipedia.page(person)
    except wikipedia.exceptions.PageError:
        print(person,'not found.')
    if len(wikipedia.search(person)) > 0:
        print('Assuming you meant',wikipedia.search('napoleona')[0])
        return wikipedia.page(wikipedia.search('napoleona')[0])
    print('Nobody found...')

def get_portrait(wikipage):
    result = requests.get('http://en.wikipedia.org/wiki/'+wikipage.title)

    #all images in infobox
    if result.status_code == requests.codes.ok:
        soup = BeautifulSoup(result.content,'lxml')
        images = soup.select('table.infobox a.image img[src]')
        portrait_link = images[0]['src']
        return 'https:'+portrait_link
    else:
        return get_portrait(wikipage)

    print('No images found on',wikipage.title)

def save_portrait(person):
    #save to local/relative directory/path.
    person_page = search(person)
    person_portrait = get_portrait(person_page)
    file_name = person_portrait.rsplit('/', 1)[-1]
    
    response = requests.get(person_portrait, stream=True)
    with open(file_name,'wb') as out_file:
        shutil.copyfileobj(response.raw,out_file)
    del response

    return([person_page.title,file_name])

def all_images(wiki_search):
    return search(wiki_search).images

def get_parents(father, mother):
    parents = []
    parents.append(save_portrait(father))
    parents.append(save_portrait(mother))
    return parents
    #print(parents)
    #dad = parents[0][1]
    #mum = parents[1][1]

def make_baby(father, mother):
    parents = get_parents(father,mother)
    if os.path.isfile(parents[0][1]) and os.path.isfile(parents[1][1]):
        print(parents[0][0],'&',parents[1][0],'are having a baby!')
        faceswap.birth(parents[0][1],parents[1][1])
    else:
        print('parents don\'t exist')
    
    
    
if __name__ == '__main__':
    parent1 = 'Adelle'# str(input('Father: ')) #sys.argv[1]
    parent2 = 'Phil Mitchell' #str(input('Mother: '))
    #search(person)
    try:
        make_baby(parent1,parent2)

##        time.sleep(3)
##        faceswap.birth(dad,mum)
        


    except wikipedia.exceptions.PageError:
        print('Could not find that person.')
        search = search(person)
        if len(search) == 0:
            print('No available suggestions')
        else:
            print('You may have meant: ', end='')
            for suggestion in search:
                print(suggestion, end='')
