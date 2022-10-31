 
from flask import Flask, jsonify, request, Response
from database.db import initialize_db
from database.models import Photo, Album
import ast
import json
from bson.objectid import ObjectId
import os
import urllib
import base64
import codecs
import sys

app = Flask(__name__)

# database configs
app.config['MONGODB_SETTINGS'] = {
    # set the correct parameters here as required, some examples are give below
    'host':'mongodb://mongo:27017/flask-database'
    # 'host':'mongodb://localhost:27017/flask-database'
}
db = initialize_db(app)

## ------
# Helper functions to be used if required
# -------
def str_list_to_album_list(str_list):
    return list(
        map(
            lambda str_item: Album.objects(id=str_item)[0],
            str_list
        )
    )

def object_list_as_id_list(obj_list):
    return list(
        map(
            lambda obj: str(obj.id),
            obj_list
        )
    )


# ----------
# PHOTO APIs
# ----------
# These methods are a starting point, implement all routes as defined in the specifications given in A+
@app.route('/listPhoto', methods=['POST'])
def add_photo():
    posted_image = request.files # "use request.files to obtain the image called file"
    posted_data = request.form # "use request.form to obtain the associated immutable dict and convert it into dict"
    body = {**posted_data}
    if 'tags' in body:
        body['tags'] = ast.literal_eval(body['tags'])
    # Check for default album
    def_album = Album.objects(name='Default')
    if not def_album: 
        def_album = Album(name='Default').save()
    if 'albums' in posted_data:
        def_album_name = str(def_album[0].id)
        complete_album_list = ast.literal_eval(posted_data['albums'])
        complete_album_list.append(def_album_name)
        body['albums'] = str_list_to_album_list(complete_album_list)
    else:
        body['albums'] = def_album
    image = {**posted_image}
    body['image_file'] = image['file']
    photo = Photo(**body).save()
    output = {'message': "Photo successfully created", 'id': str(photo.id)}
    status_code = 201
    return output, status_code

@app.route('/listPhoto/<photo_id>', methods=['GET', 'PUT', 'DELETE'])
def get_photo_by_id(photo_id):
    if request.method == "GET":
        photo = Photo.objects.get(id=photo_id)
        if photo:
            ## Photos should be encoded with base64 and decoded using UTF-8 in all GET requests with an image before sending the image as shown below
            base64_data = codecs.encode(photo.image_file.read(), 'base64')
            image = base64_data.decode('utf-8')
            ##########
            output = {'id': str(photo.id), 'name': photo.name, 'tags': photo.tags, 'location': photo.location, 'file': image, 'albums': object_list_as_id_list(photo.albums)}
            status_code = 200
            return output, status_code
    elif request.method == "PUT":
        body = request.get_json()
        keys = body.keys()
        if body and keys:
            if "tags" in keys:
                updated_body = {**body}
                updated_body['tags'] = ast.literal_eval(updated_body['tags'])
            if "albums" in keys:
                updated_body = {**body}
                def_album = Album.objects(name='Default')
                def_album_name = str(def_album[0].id)
                complete_album_list = updated_body['albums']
                complete_album_list.append(def_album_name)
                updated_body['albums'] = str_list_to_album_list(complete_album_list)
            Photo.objects.get(id=photo_id).update(**updated_body)
        output = {'message': "Photo successfully updated", 'id': str(photo_id)}
        status_code = 200
        return output, status_code
    elif request.method == "DELETE":
        photo = Photo.objects.get(id=photo_id)
        photo.delete()
        output = {'message': "Photo successfully deleted", 'id': str(photo_id)}
        status_code = 200
        return output, status_code

@app.route('/listPhotos', methods=['GET'])
def get_photos():
    tag = request.args.get("tag", default="", type=str) # "Get the tag from query parameters" 
    albumName = request.args.get("albumName", default="", type=str) # "Get albumname from query parameters"
    if albumName != "":
        album = Album.objects(name=albumName)
        photos = Photo.objects(albums=album[0])
        photo_objects = Photo.objects(albums=Album.objects(name=albumName)[0])
    elif tag != "":
        photo_objects = Photo.objects(tags=tag)
    else:
        photo_objects = Photo.objects()
    photos = []
    for photo in photo_objects:
        try:
            base64_data = codecs.encode(photo.image_file.read(), 'base64')
            image = base64_data.decode('utf-8')
        except:
            image = ""
        photos.append({'name': photo.name, 'location': photo.location, 'file': image})
    return jsonify(photos), 200

# ----------
# ALBUM APIs
# ----------
# Complete the album APIs similarly as per the instructions provided in A+
@app.route('/listAlbum', methods=['POST'])
def add_album():
    posted_data = request.get_json() # "use request.form to obtain the associated immutable dict and convert it into dict"
    body = {**posted_data}
    album = Album(**body).save()
    output = {'message': "Album successfully created", 'id': str(album.id)}
    status_code = 201
    return output, status_code

@app.route('/listAlbum/<album_id>', methods=['GET', 'PUT', 'DELETE'])
def get_album_by_id(album_id):
    if request.method == "GET":
        album = Album.objects.get(id=album_id)
        output = {'id': str(album.id), 'name': album.name}
        status_code = 200
        return output, status_code
    elif request.method == "PUT":
        body = request.get_json()
        Album.objects.get(id=album_id).update(**body)
        output = {'message': "Album successfully updated", 'id': str(album_id)}
        status_code = 200
        return output, status_code
    elif request.method == "DELETE":
        album = Album.objects.get(id=album_id)
        album.delete()
        output = {'message': "Album successfully deleted", 'id': str(album_id)}
        status_code = 200
        return output, status_code


# Only for local testing without docker
# app.run() # FLASK_APP=app.py FLASK_ENV=development flask run
