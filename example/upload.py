import os
import requests
import copy
import time
from flask import Flask, render_template, jsonify
from flask import request, send_from_directory, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES
from PIL import Image


app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
preview = UploadSet('preview', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
app.config['UPLOADED_PREVIEW_DEST'] = 'static/preview'

app.config['UPLOADED_PHOTOS_SCALE_100'] = 'static/images/scale_100'
app.config['UPLOADED_PHOTOS_SCALE_50'] = 'static/images/scale_50'
app.config['UPLOADED_PHOTOS_SCALE_20'] = 'static/images/scale_20'

configure_uploads(app, photos)

def imageResizer(im, pixellimit):

  width, height = im.size

  if width > height:
    #Land scape mode. Scale to width.

    aspectRatio = float(height)/float(width)
    Scaledwidth = pixellimit
    Scaledheight = int(round(Scaledwidth * aspectRatio))
    newSize = (Scaledwidth, Scaledheight)
  elif height > width:
    #Portrait mode, Scale to height.
    aspectRatio = float(width)/float(height)
    Scaledheight = pixellimit
    Scaledwidth = int(round(Scaledheight * aspectRatio))
    newSize = (Scaledwidth, Scaledheight)

  #FAILS RIGHT HERE... I double checked by writing print flags all over, and it so happens nothing past this line gets written
  imageThumbnail = im.resize(newSize)

  return imageThumbnail



@app.route('/')
@app.route('/index')
def show_index():
    # images = os.listdir(app.config['UPLOADED_PREVIEW_DEST'])
    # r = requests.get('http://127.0.0.1:5000/api/preview')
    # print(r.status_code)
    # if r.status_code == 200:
    # data = r.json()
    # images = data.get('images')
    # print(images)
    return render_template("index.html")



@app.route('/preview/<scale>/<image_id>')
def preview(scale, image_id):
    if str(scale) == '100':
        return send_from_directory(app.config['UPLOADED_PHOTOS_SCALE_100'], image_id)
    else:
        return send_from_directory(app.config['UPLOADED_PHOTOS_SCALE_20'], image_id)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        origin = photos.save(request.files['photo'], name='origin_.png')
        return origin
    return render_template('upload.html')


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
        imageThumbnail = imageResizer(image, 200)
        image_name = request.files['photo'].filename
        # pre_name = 'pre_{}'.format(image_name)
        imageThumbnail.save(os.path.join(
        app.config['UPLOADED_PHOTOS_SCALE_20'], image_name))
        # ori_name = 'ori_{}'.format(image_name)
        image.save(os.path.join(
        app.config['UPLOADED_PHOTOS_SCALE_100'], image_name))
        return jsonify(image_id=image_name, status=100, info='ok')
    else:
        return jsonify(status=101, info='failure')


if __name__ == '__main__':
    app.run(debug=True)
