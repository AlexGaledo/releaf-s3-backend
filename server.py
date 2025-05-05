from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import boto3
import os
import uuid

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://releaf-react.vercel.app/"])

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=os.environ.get('AWS_REGION')
)

#local debug function
@app.route('/list-files', methods=['GET'])
def list_files():
    try:
        response = s3.list_objects_v2(Bucket='releaf-bucket')
        contents = [obj['Key'] for obj in response.get('Contents', [])]
        return jsonify({'files': contents})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload-image', methods=['POST'])
def upload_file():
    key = request.args.get('projectID')
    if not key:
        return jsonify({'response' : 'need project id'})
    
    file = request.files.get('file')
    if not file:
        return jsonify({'response': 'requires uploaded file'})

    # Use fixed filename for consistent referencing
    file_extension = file.filename.split('.')[-1]
    s3_key = f'projects/{key}/preview.{file_extension}'
    bucket = 'releaf-bucket'

    try:
        s3.upload_fileobj(
            file,
            bucket,
            s3_key,
            ExtraArgs={'ACL': 'public-read'}  # <--- Make it publicly accessible
        )
        return jsonify({
            'response': 'file successfully uploaded',
            'url': f'https://{bucket}.s3.amazonaws.com/{s3_key}'
        })
    except Exception as e:
        return jsonify({'response':'error interacting with s3 storage', 'error': str(e)}), 500



@app.route('/get-image', methods=['GET'])
def get_image():
    key = request.args.get('projectID')
    #return error if key is not presented
    if not key:
       return jsonify({'response':'requires key to retrieve image'})


    s3_key = f'projects/{key}/preview.jpg'
    try:
        
        url = f'https://releaf-bucket.s3.amazonaws.com/{s3_key}'

        return jsonify({
            'response': 'success',
            'message': 'Image retrieved',
            'projectID': key,
            'url': url
        })
    
    except Exception as e:
        return jsonify({ 'error':str(e)}),500    
    


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to ReLeaf backend API'})        
    

if __name__ == '__main__':
    app.run(debug=True)

