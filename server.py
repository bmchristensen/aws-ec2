# import requests
import boto3

from flask import Flask
from flask import jsonify
# from flask import request
from flask_cors import CORS


DEBUG = True
BUCKET = "cloud-dev-bucket-s3bucket-1sifmcfkfvav1"

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


def build_object(obj, value):
    last_index = len(value)
    print(value)

    for i in range(0, last_index - 1):
        key = value[i]

        if key in obj:
            print("key in obj")
        else:
            print("key is in obj")
            print("key = ", key)
            obj[key] = {}

        obj = obj[key]
        print("obj = ", obj)

    obj[value[last_index - 1]] = "value"


@app.route('/music', methods=['GET'])
def return_music():
    s3 = boto3.client('s3')
    s3_objects = s3.list_objects_v2(Bucket=BUCKET)
    objects = s3_objects.get('Contents')
    response = {}

    for obj in objects:
        this_obj = obj.get('Key').rsplit(sep='/')

        build_object(response, this_obj)
        print("response = ", response)

    return jsonify(response)


if __name__ == "__main__":
    app.run()
