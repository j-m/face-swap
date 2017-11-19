# luckyface.py - Will go through google images until it finds a valid face.

# TRY EXCEPT IN GET PORTRAIT
# _gdf kno-fb-ctx

import os
import requests
import shutil
import wikipedia
import cv2
import re
from bs4 import BeautifulSoup

import faceswap

def get_valid_portrait(person):
    try:
        wikipedia.page(person)
        page = wikipedia.page(person)
    except wikipedia.exceptions.PageError:
        print(person,'not found.')
        if len(wikipedia.search(person)) > 0:
            print('Assuming you meant',wikipedia.search(person)[0])
            page = wikipedia.page(wikipedia.search(person)[0])
    #print('Nobody found...')

    result = requests.get('http://en.wikipedia.org/wiki/'+page.title)

    #all images in infobox
    if result.status_code == requests.codes.ok:
        soup = BeautifulSoup(result.content,'lxml')
        images = soup.select('img[src]') #table.infobox a.image 
        #'https:'
        for img in images:
            if img['src'][-3:] != 'png' and img['src'][-3:] != 'jpg':
                continue
            #print(img['src'])
            if 'svg' in img['src'] or 'static' in img['src']:
                continue
            response = requests.get('https:'+img['src'], stream=True)
            #print(img['src'])
            with open('dump.jpg','wb') as out_file:
                shutil.copyfileobj(response.raw,out_file)
            try:
                im = cv2.imread('dump.jpg', cv2.IMREAD_COLOR)
##                if not im:
##                    continue
                im = cv2.resize(im, (im.shape[1] * 1, im.shape[0] * 1))
                try:
                    #print('--')
                    faceswap.get_landmarks(im)
                    #os.rename('dump.jpg',person+'.jpg')
                    img_link = 'https:'+img['src']
                    #print(type(img_link))
                    return img_link
                    #print('--',img)
                except RuntimeError:
                    continue
                    #print('Not 8bit gray or RGB')
            except faceswap.TooManyFaces:
                continue
                #print('Too many face...')
            except faceswap.NoFaces:
                continue
                #print('No faces...')

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
    #print(person)
    #save to local/relative directory/path.
    person_page = search(person)
    print(person_page)
    person_portrait = get_valid_portrait(person_page)#person_page
    file_name = person_page#person_portrait.rsplit('/', 1)[-1]
    
    response = requests.get(person_portrait, stream=True)
    with open(file_name,'wb') as out_file:
        shutil.copyfileobj(response.raw,out_file)
    del response

    try:
        person_summary = person_summary.title+' is a '+get_proffession(person_summary.title)
    except Exception:
        person_summary = wikipedia.page(person_page).summary
    
    return([person_page,person_summary])#person_page


def all_images(wiki_search):
    return search(wiki_search).images


def get_parents(father, mother):
    parents = [save_portrait(father), save_portrait(mother)]
    return parents


def make_baby(father, mother, out_path="child.jpg"):
    parents = get_parents(father, mother)
    if os.path.isfile(parents[0][1]) and os.path.isfile(parents[1][1]):
        print(parents[0][0], '&', parents[1][0], 'are having a baby!')
        faceswap.birth(parents[0][1], parents[1][1], out_path)
        parent_info = []
        for p in parents:
            name = p[0]
            p = p[1].split('\n')
            a = p[:2]
            skills = re.search(r'(was an |was a |is a |is an )(.*)',a[0]).group(2)
            skills = skills.split('.')[0]
            #print(p[0],skills)
            parent_info.append([name,skills])
        print(parent_info)
        return parent_info
    else:
        print('parents don\'t exist')


if __name__ == '__main__':
    parent1 = 'hitler'
    parent2 = 'Phil Mitchell'
    try:
        make_baby(parent1, parent2)
    except:
        print('Error')
