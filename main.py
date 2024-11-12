from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import time
import hashlib
import re
from werkzeug.utils import safe_join


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads' 
MAX_FILE_SIZE = 1024 * 1024 
MAX_FOLDER_SIZE = 1024 * 1024 * 1024  

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

def manage_storage():
    """Deletes the oldest file in the upload folder if the total size exceeds the limit."""
    folder_size = 0
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(filepath):
            filesize = os.path.getsize(filepath)
            folder_size += filesize
            files.append((filepath, filesize))

    if folder_size > MAX_FOLDER_SIZE:
        oldest_file = min(files, key=lambda x: os.path.getmtime(x[0])) 
        os.remove(oldest_file[0])
        print(f"Deleted oldest file: {oldest_file[0]} to manage storage.")

def is_regular_text(text):
    if not isinstance(text, str):
        return False
    return bool(re.match('[^\w]', text))

@app.route('/api/upload', methods=['POST'])
def upload_file():
    manage_storage() 

    if 'audio' not in request.files:
        return jsonify({'message': 'No audio file provided'}), 400
    
    file = request.files['audio']

    if is_regular_text(file.filename):
        return jsonify({'message': 'Invalid file name'}), 400
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if len(file.read()) > MAX_FILE_SIZE: 
        return jsonify({'message': 'File size exceeds 1MB limit'}), 413 
    print(file.filename)
    file.seek(0)
    file_content = file.read()
    file.seek(0)
    file_hash = hashlib.sha256(file_content).hexdigest()

    for existing_filename in os.listdir(app.config['UPLOAD_FOLDER']):
        existing_filepath = safe_join(app.config['UPLOAD_FOLDER'], existing_filename)
        if os.path.isfile(existing_filepath):
            with open(existing_filepath, 'rb') as f:
                existing_content = f.read()
                existing_hash = hashlib.sha256(existing_content).hexdigest()
                if file_hash == existing_hash:
                    return jsonify({'message': 'An identical recording already exists.'}), 409 
    
    filename = safe_join(app.config['UPLOAD_FOLDER'], str(int(time.time()))+"-"+file.filename)

    try:
        file.save(filename)
    except Exception as e:
        return jsonify({'message': f"Error saving file: {str(e)}"}), 500
    return jsonify({'message': 'File uploaded successfully'}), 201

@app.route('/api/recordings')
def list_recordings():
    """Returns a list of available recordings."""
    try:
        recordings = [
            f for f in os.listdir(app.config['UPLOAD_FOLDER'])
            if os.path.isfile(safe_join(app.config['UPLOAD_FOLDER'], f)) 
        ]
        return jsonify(recordings)

    except FileNotFoundError: 
        return jsonify({'message': "Uploads directory not found"}), 500 
    except Exception as e:
        return jsonify({'message': f"Error listing recordings: {str(e)}"}), 500

@app.route("/recordings")
def rec():
    return render_template('recordings.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory("",safe_join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
