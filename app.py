from flask import Flask, flash, request, redirect, url_for, render_template, session, jsonify, make_response
from werkzeug.utils import secure_filename
from photo_restorer import predict_image
from datetime import datetime, timedelta
import os

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.secret_key = 'djdj#$+$8$8jdj7#8#jejs'

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to check if the user has exceeded the maximum limit of predictions per day
def check_prediction_limit():
    if 'prediction_count' not in session:
        session['prediction_count'] = 0
    return session['prediction_count'] >= 1#2

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

            # Check if the user has exceeded the prediction limit for the day
            if check_prediction_limit():
                return render_template("limit-exceeded.html")

            predicted_img_url = predict_image(full_filename)
            session['prediction_count'] = session.get('prediction_count', 0) + 1

            # Create a response object and set the session cookie
            response = make_response(render_template("display-page.html", filename=filename, restored_img_url=predicted_img_url), 200)
            session_id = session.get('session_id')
            if not session_id:
                session_id = os.urandom(16).hex()
                session['session_id'] = session_id
            response.set_cookie('session_id', session_id, expires=datetime.now() + timedelta(days=1))

            return response

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
















