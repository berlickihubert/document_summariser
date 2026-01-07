from flask import Flask, render_template, request, jsonify
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)
BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

@app.route('/')
def home():
    files = []
    if BUCKET_NAME:
        try:
            response = s3.list_objects_v2(Bucket=BUCKET_NAME)
            files = [obj['Key'] for obj in response.get('Contents', [])]
        except Exception as e:
            print(f"Error fetching files from S3: {e}")

    return render_template('index.html', files=files)

@app.route('/summarize', methods=['POST'])
def summarize():
    selected_file = request.form.get('selected_file')
    file = request.files.get('file')

    if not file and not selected_file:
         return jsonify({'error': 'No file uploaded or selected'}), 400
    
    filename = ""

    if file and file.filename != '':
        filename = file.filename
        try:
            if not BUCKET_NAME:
                 return jsonify({'error': 'S3_BUCKET_NAME not configured'}), 500
            file.seek(0)
            s3.upload_fileobj(file, BUCKET_NAME, filename)
        except Exception as e:
             return jsonify({'error': f"Failed to upload: {str(e)}"}), 500
    
    elif selected_file:
        filename = selected_file
        pass 

    summary = f"File '{filename}' processed. Future LLM integration will reside here."
    
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
