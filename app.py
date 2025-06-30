from flask import Flask, request, render_template, redirect, url_for  # Flask, a simple web framework that helps you build web apps using Python 
# We are importing tools (request, render_template, redirect, url_for) from Flask

import boto3 # boto3 is python SDK (toolkit) for our python script to interact with AWS services like S3, EC2, DynamoDB

from botocore.exceptions import NoCredentialsError, ClientError  # botocore.exceptions is part of the Boto3 library. 

# It will throw no credentials error if probably you forgot to put in the Access keys or IAM role. 

app = Flask(__name__)  # creates a new Flask web application, using the current file's name (app.py) to let Flask know where to find resources like templates and static files.

# __name__ is a special python variable

# Replace this with your actual S3 bucket name
S3_BUCKET_NAME = 'your-bucket-name'


s3_client = boto3.client('s3')  # creates an object (S3 client) using Boto3 to allow the web app perform actions like upload_file, get_object() etc. 

@app.route('/')  # tells Flask to run a specific function when someone visits the home page ("/") of the web app.
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

if __name__ == '__main__':         # ensures that the code inside it only runs when the script is executed directly, not when it's imported as a module in another script.
    app.run(host='0.0.0.0', port=5000, debug=True)  # starts the Flask web server, making it accessible from any IP (0.0.0.0) on port 5000, with debug mode enabled for live updates and error messages
