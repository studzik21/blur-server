from flask import Flask, request, after_this_request
import os

from upload import upload_file_to_s3
from blur_faces import blur

app = Flask(__name__)

UPLOAD_FOLDER = 'uploaded'
BLURED_FOLDER = 'blured'

def index():
    return "Blur server!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        uploaded_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(uploaded_file_path)

        if not os.path.exists(BLURED_FOLDER):
            os.makedirs(BLURED_FOLDER)
        blured_file_path = os.path.join(BLURED_FOLDER, file.filename)
        blur(uploaded_file_path, blured_file_path)
        url = upload_file_to_s3(blured_file_path, file.filename)

        @after_this_request
        def delete(response):
            os.remove(uploaded_file_path)
            os.remove(blured_file_path)
            return response

        return url
    else:
        return 'No file in request.'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
