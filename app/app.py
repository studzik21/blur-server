from flask import Flask, request, send_from_directory, url_for
import os
from dotenv import load_dotenv

from upload import upload_file_to_s3
from blur_faces import blur

app = Flask(__name__)

UPLOAD_FOLDER = 'files'
TMP_FOLDER = 'tmp'
server_address = "local"


def index():
    return "Hello World!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        if not os.path.exists(TMP_FOLDER):
            os.makedirs(TMP_FOLDER)
        original_file_name = os.path.join(TMP_FOLDER, file.filename)
        file.save(original_file_name)

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        path_to_blured = os.path.join(UPLOAD_FOLDER, file.filename)
        blur(original_file_name, path_to_blured)
        url = upload_file_to_s3(path_to_blured, file.filename)
        return url
    else:
        return 'No file in request.'


@app.route('/files/<filename>')
def send_blured_movie(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
