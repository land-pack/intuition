import os
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
    images = os.listdir(app.config['UPLOADED_PREVIEW_DEST'])
    return render_template("index.html", images = images)



@app.route('/preview/<image_id>')
def preview(image_id):
    return send_from_directory(app.config['UPLOADED_PREVIEW_DEST'], image_id)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        origin = photos.save(request.files['photo'], name='origin_.png')
        return origin
    return render_template('upload.html')


@app.route('/api/preview')
def api_preview():
    images = os.listdir(app.config['UPLOADED_PREVIEW_DEST'])
    images_url = [url_for('preview', image_id=image_id) for image_id in images]
    return jsonify(items=len(images_url), images=images_url,
        status=100, info='ok')

@app.route('/api/upload', methods=['POST'])
def api_upload():
    if 'photo' in request.files:
        image = Image.open(request.files['photo'])
        imageThumbnail = imageResizer(image, 200)
        image_name = request.files['photo'].filename
        imageThumbnail.save(os.path.join(
        app.config['UPLOADED_PREVIEW_DEST'], image_name))

        image.save(os.path.join(
        app.config['UPLOADED_PHOTOS_DEST'], image_name))
        return jsonify(image_id=image_name,status=100, info='ok')
    else:
        return jsonify(status=101, info='failure')


if __name__ == '__main__':
    app.run(debug=True)
