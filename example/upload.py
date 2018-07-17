import os
import time
from flask import Flask, render_template, request, send_from_directory, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES


app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/')
@app.route('/index')
def show_index():
    images = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])
    print(url_for('preview', image_id='orgin__1.png'))
    return render_template("index.html", images = images)

@app.route('/preview/<image_id>')
def preview(image_id):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], image_id)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        origin = photos.save(request.files['photo'], name='origin_.png')
        return origin
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)