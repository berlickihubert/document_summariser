from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = file.filename
        content_length = len(file.read())
        
        summary = f"This is a placeholder summary for the file '{filename}' which is {content_length} bytes long. Future LLM integration will reside here."
        
        return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
