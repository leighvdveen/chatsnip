from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from extractor import extract_chat_from_json_stream  # Import from extractor.py

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            chat_name = request.form['chat_name']
            extracted_text = extract_chat_from_json_stream(file_path, chat_name)
            
            if extracted_text:
                output_file = os.path.join(app.config['UPLOAD_FOLDER'], f'{chat_name}.txt')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)
                return send_file(output_file, as_attachment=True)
            else:
                return "Chat not found or content could not be extracted."
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)