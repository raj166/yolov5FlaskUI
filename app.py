import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
from subprocess import call, run
from PIL import Image
image_list= ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo']
app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.jpeg' , '.mp4']
app.config['UPLOAD_PATH'] = 'uploads'

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
                pass
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        print(file_path)
        # image = Image.open(file_path)
        # image.save(file_path)
        if (any(image_list in file_path for image_list in image_list)):
            image = Image.open(file_path)
            image = image.resize((640, 640))
            image.save(file_path)
        run(["python3", "detect.py", "--source",  file_path, "--view-img","--class", "0", "1", "2", "3", "4", "5", "6", "7", "8" , "--view-img"])
        #run(["python3", "awsdetect.py", "--source",  file_path, "--class", "0", "1", "2", "3", "4", "5", "6", "7", "8", "--view-img", "--name", "output/"])
        
        #image Enhancemnet
        #run(["python3", "image_enhancement.py", "--filename", file_path, "--output", "./output/name.jpg", "--display", "0"])
        #run(["python3", "image_enhancement.py", "--filename", file_path, "--output", "./output/name.jpg", "--display", "1"])
    return '', 204
    

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)
    
if __name__ == '__main__':  
    app.run(host = '0.0.0.0', port = 5555)
