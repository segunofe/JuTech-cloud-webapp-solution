from flask import Flask, request, render_template, redirect, url_for
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

app = Flask(__name__)

# Replace this with your actual S3 bucket name
S3_BUCKET_NAME = 'your-bucket-name'

# Initialize the S3 client using IAM role credentials (auto from EC2 metadata)
s3_client = boto3.client('s3')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    try:
        # Upload file to S3
        s3_client.upload_fileobj(
            file,
            S3_BUCKET_NAME,
            file.filename
        )
        return redirect(url_for('index'))
    
    except NoCredentialsError:
        return "IAM role credentials not available"
    except ClientError as e:
        return f"AWS error occurred: {e.response['Error']['Message']}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
