from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import boto3
import os

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

@app.route('/list-files', methods=['GET'])
def list_files():
    try:
        response = s3.list_objects_v2(Bucket='releaf-bucket')
        contents = [obj['Key'] for obj in response.get('Contents', [])]
        return jsonify({'files': contents})
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('upload-image', methods=['POST'])
def upload_file(key):
    file = request.files['file']
    bucket = 'releaf-bucket'
    s3_key = file.filename
    return jsonify({'response':'file successfully uploaded'})


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to ReLeaf backend API'})        
    

if __name__ == '__main__':
    app.run(debug=True)

