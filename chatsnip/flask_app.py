from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from chatsnip.extractor import extract_chat_from_json_stream  # Import from extractor.py

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/extract_chat', methods=['POST'])
def extract_chat():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        chat_name = request.form['chat_name']
        extracted_text = extract_chat_from_json_stream(file_path, chat_name)
        
        if extracted_text:
            return extracted_text, 200
        else:
            return "Chat not found or content could not be extracted.", 400

if __name__ == "__main__":
    app.run(debug=True)