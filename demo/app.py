import requests
from flask import Flask, render_template



app = Flask(__name__)



@app.route("/")
def index():
    r = requests.get('http://127.0.0.1:5001/api/preview')
    data = r.json()
    images = data.get('images')
    return render_template('index.html', images=images)


@app.route("/upload")
def upload():
    return render_template('upload.html')



if __name__ == '__main__':
    app.run(debug=True)
