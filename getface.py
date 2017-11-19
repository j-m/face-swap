import cv2
import os
import requests
import shutil
import wikipedia
from bs4 import BeautifulSoup

import faceswap


def get_portrait(person):
    try:
        wikipedia.page(person)
        page = wikipedia.page(person)
    except wikipedia.exceptions.PageError:
        print(person, 'not found.')
    if len(wikipedia.search(person)) > 0:
        print('Assuming you meant', wikipedia.search(person)[0])
        page = wikipedia.page(wikipedia.search(person)[0])

    result = requests.get('http://en.wikipedia.org/wiki/' + page.title)

    # All images in infobox
    if result.status_code == requests.codes.ok:
        soup = BeautifulSoup(result.content, 'lxml')
        images = soup.select('img[src]')  # table.infobox a.image
        # 'https:'
        for img in images:
            if img['src'][-3:] != 'png' and img['src'][-3:] != 'jpg':
                continue
            # print(img['src'])
            if 'svg' in img['src'] or 'static' in img['src']:
                continue
            response = requests.get('https:' + img['src'], stream=True)
            # print(img['src'])
            with open('dump.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            try:
                im = cv2.imread('dump.jpg', cv2.IMREAD_COLOR)
                im = cv2.resize(im, (im.shape[1] * 1, im.shape[0] * 1))
                try:
                    # print('--')
                    faceswap.get_landmarks(im)
                    os.rename('dump.jpg', person + '.jpg')
                    # print('--',img)
                except RuntimeError:
                    continue
                    # print('Not 8bit gray or RGB')
            except faceswap.TooManyFaces:
                continue
                # print('Too many face...')
            except faceswap.NoFaces:
                continue
                # print('No faces...')


if __name__ == '__main__':
    get_portrait('ariana grande')
