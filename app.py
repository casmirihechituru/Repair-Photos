from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, make_response
from werkzeug.utils import secure_filename
from photo_restorer import predict_image
import os

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload-page')
def upload_page():
    return render_template('upload-page.html')

@app.route('/display-page', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_filename = "." + url_for("static", filename="images/" + filename)
            file.save(full_filename)

            predicted_img_url = predict_image(full_filename)

            return render_template("display-page.html", filename=filename, restored_img_url=predicted_img_url)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
