#! python3
# luckyface.py - Will go through google images until it finds a valid face.

import sys, wikipedia, shutil, requests

def search(person):
    return(wikipedia.search(person))

images = wikipedia.WikipediaPage('Phil Mitchell').images

def get_portrait(images):
    for im in images:
        if im[-3] == 'png' or im[-3:] == 'jpg':
            print(im)
            return im
    print('No images found for',person)


if __name__ == '__main__':
    person = sys.argv[1]
    search(person)
    try:
        person_page = wikipedia.page(person)
        person_portrait = get_portrait(person_page.images)
        print(person_portrait.rsplit('/', 1)[-1])
        #response = requests.get(person_portrait.rsplit('/', 1)[-1], stream=True)
        
    except wikipedia.exceptions.PageError:
        print('Could not find that person.')
        search = search(person)
        if len(search) == 0:
            print('No available suggestions')
        else:
            print('You may have meant: ', end='')
            for suggestion in search:
                print(suggestion, end='')
