# import requests
import boto3
import urllib
import json

from flask import Flask
from flask import jsonify
# from flask import request
from flask_cors import CORS


DEBUG = True
BUCKET = "cloud-dev-bucket-s3bucket-1sifmcfkfvav1"

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


def objectify(obj, artist_album_song, url):
    last = len(artist_album_song) - 1

    for this_artist_album_song in artist_album_song:
        if this_artist_album_song is artist_album_song[last]:
            break
        elif this_artist_album_song not in obj:
            obj[this_artist_album_song] = {}

        obj = obj[this_artist_album_song]

    obj[artist_album_song[last]] = url


@app.route('/music', methods=['GET'])
def return_music():
    s3 = boto3.client('s3')
    s3_response = s3.list_objects_v2(Bucket=BUCKET).get('Contents')
    response = {}

    for obj in s3_response:
        link = obj.get('Key')
        this_obj = link.rsplit(sep='/')
        url_str = "https://{}.{}/{}".format(BUCKET, 's3.amazonaws.com', link)
        url = url_str.replace(" ", "+")
        objectify(response, this_obj, url)

    return jsonify(response)


if __name__ == "__main__":
    # app.run()
    app.run(host="0.0.0.0", port=80)
