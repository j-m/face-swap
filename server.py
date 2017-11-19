from flask import Flask, request
import json
import cloudinary
import cloudinary.uploader
import string
import random
import luckyface
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# cloudinary.config(
#     cloud_name=os.environ['CLOUDINARY_CLOUD_NAME'],
#     api_key=os.environ['CLOUDINARY_API_KEY'],
#     api_secret=os.environ['CLOUDINARY_API_SECRET']
# )


def write_cache(father, mother, image_url, filename):
    filename = 'combinations.json'
    key = "%s and %s" % (father, mother)

    with open(filename, 'r') as jsonFile:
        data = json.load(jsonFile)

    try:
        data[key]
    except KeyError:
        data[key] = {
            'url': image_url,
            'filename': filename
        }

    with open(filename, 'w') as jsonFile:
        json.dump(data, jsonFile)


def get_cached_url(father, mother):
    filename = 'combinations.json'
    key = "%s and %s" % (father, mother)

    with open(filename, 'r') as jsonFile:
        data = json.load(jsonFile)

    try:
        dictionary = data[key]
    except:
        return None

    try:
        url = dictionary['url']
    except:
        return None

    return url


def bad():
    return str({
        'status': 'error'
    }), 400


def good(url):
    return str({
        'status': 'OK',
        'image_url': url
    }), 200


def generate_child(father, mother):
    filename = 'imgz' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20)) + '.jpg'
    luckyface.make_baby(father, mother, filename)
    return filename


def upload_image(filename):
    try:
        url = cloudinary.uploader.upload(filename)['url']
        return url
    except Exception as e:
        return None


@app.route('/get-child')
def get_child():
    try:
        father, mother = request.args.get('father'), request.args.get('mother')
    except:
        return bad()

    if not mother or not father:
        return bad()

    url = get_cached_url(father, mother)
    if url:
        return good(url)

    filename = generate_child(father, mother)

    url = upload_image(filename)

    if url:
        write_cache(father, mother, url, filename)
        print(url)
        return good(url)

    return bad()

