# import requests
import boto3
import urllib

from flask import Flask
from flask import jsonify
# from flask import request
from flask_cors import CORS


DEBUG = True
BUCKET = "cloud-dev-bucket-s3bucket-1sifmcfkfvav1"

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


def build_object(obj, value, url):
    last_index = len(value) - 1

    for i in range(0, last_index):
        key = value[i]

        if key in obj:
            print("key in obj")
        else:
            obj[key] = {}

        obj = obj[key]

    obj[value[last_index]] = url


@app.route('/music', methods=['GET'])
def return_music():
    s3 = boto3.client('s3')
    s3_objects = s3.list_objects_v2(Bucket=BUCKET)
    objects = s3_objects.get('Contents')
    response = {}

    for obj in objects:
        link = obj.get('Key')
        this_obj = link.rsplit(sep='/')
        url_string = "https://{}/{}".format(BUCKET, link)
        url = urllib.parse.quote_plus(url_string)

        build_object(response, this_obj, url)

    return jsonify(response)


if __name__ == "__main__":
    # app.run()
    app.run(host="0.0.0.0", port=80)
