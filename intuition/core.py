import os
import requests
import copy
import time
from flask import Flask, render_template, jsonify
from flask import request, send_from_directory, url_for
from PIL import Image
from utils import image_resize


app = Flask(__name__)

app.config['UPLOADED_PHOTOS_SCALE_100'] = 'static/images/scale_100'
app.config['UPLOADED_PHOTOS_SCALE_50'] = 'static/images/scale_50'
app.config['UPLOADED_PHOTOS_SCALE_20'] = 'static/images/scale_20'






@app.route('/preview/<scale>/<image_id>')
def preview(scale, image_id):
    if str(scale) == '100':
        return send_from_directory(app.config['UPLOADED_PHOTOS_SCALE_100'], image_id)
    else:
        return send_from_directory(app.config['UPLOADED_PHOTOS_SCALE_20'], image_id)


@app.route('/api/preview')
def api_preview():
    # List all origin image by it's name
    images = os.listdir(app.config['UPLOADED_PHOTOS_SCALE_100'])
    images_url = [
        (url_for('preview', scale=100 ,image_id= image_id),
        url_for('preview', scale=20, image_id= image_id))
    for image_id in images]


    return jsonify(items=len(images_url), images=images_url,
        status=100, info='ok')

@app.route('/api/upload', methods=['POST'])
def api_upload():
    if 'photo' in request.files:
        image = Image.open(request.files['photo'])
        imageThumbnail = image_resize(image, 200)
        image_name = request.files['photo'].filename
        imageThumbnail.save(os.path.join(
        app.config['UPLOADED_PHOTOS_SCALE_20'], image_name))
        image.save(os.path.join(
        app.config['UPLOADED_PHOTOS_SCALE_100'], image_name))
        return jsonify(image_id=image_name, status=100, info='ok')
    else:
        return jsonify(status=101, info='failure')


if __name__ == '__main__':
    app.run(debug=True)
