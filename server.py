from flask import Flask, request
# import cloudinary

app = Flask(__name__)


@app.route('/get-child')
def get_child():
    return 'url', 200

