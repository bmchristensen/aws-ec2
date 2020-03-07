# import requests
import boto3
import urllib
import json

from boto3.dynamodb.conditions import Key, Attr
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

BUCKET = "cloud-dev-bucket-s3bucket-1sifmcfkfvav1"
DB = 'music'
DB_USER = 'users'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app)


def build_url(path):
    url_str = 'https://{}.{}/{}'.format(BUCKET, 's3.amazonaws.com', path)
    url = url_str.replace(' ', '+')

    return url


def objectify(obj, artist_album_song, url):
    song = len(artist_album_song) - 1

    for this_artist_album_song in artist_album_song:
        if this_artist_album_song is artist_album_song[song]:
            break
        elif this_artist_album_song not in obj:
            obj[this_artist_album_song] = {}

        obj = obj[this_artist_album_song]

    obj[artist_album_song[song]] = url


def db_query(**params):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(DB)

    response = table.query(
        KeyConditionExpression=Key(params.get('pk')).eq(params.get('sk'))
    )

    item = response['Items']

    return item


def responsify(response):
    ret = list()
    for each in response:
        ret.append(each.get('sk'))

    return ret


@app.route('/music', methods=['GET'])
def return_music():
    s3 = boto3.client('s3', region_name='us-east-1')
    s3_response = s3.list_objects_v2(Bucket=BUCKET).get('Contents')
    response = {}

    for obj in s3_response:
        link = obj.get('Key')
        this_obj = link.rsplit(sep='/')
        url = build_url(link)
        objectify(response, this_obj, url)

    return jsonify(response)


@app.route('/genres', methods=['GET'])
def genres():
    response = db_query(pk='pk', sk='Genre')

    return jsonify(responsify(response))


@app.route('/artists/by/genre/', methods=['GET'])
def artists_by_genre():
    genre = request.args.get('genre', type=str)
    response = db_query(pk='pk', sk=genre)

    return jsonify(responsify(response))


@app.route('/albums/for/artist', methods=['GET'])
def albums_for_artist():
    artist = request.args.get('artist', type=str)
    response = db_query(pk='pk', sk=artist)

    return jsonify(responsify(response))


@app.route('/songs/for/album', methods=['GET'])
def songs_for_album():
    album = request.args.get('album', type=str)
    response = db_query(pk='pk', sk=album)

    return jsonify(responsify(response))


@app.route('/song', methods=['GET'])
def song():
    song = request.args.get('song', type=str)
    response = db_query(pk='pk', sk=song)
    link = response[0].get('sk')
    url = build_url(link)

    return jsonify(url)


if __name__ == "__main__":
    # app.run()
    app.run(host="0.0.0.0", port=80)
