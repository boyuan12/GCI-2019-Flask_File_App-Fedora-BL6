import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from os import path

UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return '<h1>No file Uploaded</h1>'
        file = request.files['file']
        filename = request.form.get('filename')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/read/' + filename)
    else:
        files = os.listdir('./upload')
        return render_template('index.html', files=files)

@app.route('/read/<string:filename>')
def read(filename):
    try:
        file = open('./upload/' + filename, "r")
        contents = file.read()
        return '<h1>' +  filename +'</h1><br>' + contents
    except FileNotFoundError:
        return '<h1 style="color: red;"> File Not Found </h1>'