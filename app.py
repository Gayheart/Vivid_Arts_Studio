from flask import Flask, render_template, request, flash
import boto3
from werkzeug.utils import secure_filename
from time import sleep
import os


# Setting Up credentials
#NB: create new py file to hold credentials as var, import to use, gitignore that file

s3 = boto3.client(
    "s3",
    # aws_access_key_id="",
    # aws_secret_access_key="",
    # Boto# checks env var
)

# Bucket to be used (create via terraform and not boto3)
UNPROCESSED_BUCKET_NAME = "vivid-arts-unprocessed"
PROCESSED_BUCKET_NAME = "vivid-arts-processed"

app = Flask(__name__)
images_folder = os.path.join('static', 'images')
 
app.config['IMAGES'] = images_folder

@app.route('/')
def index():
    return render_template('index.html')


# Uploading to S3

@app.route('/upload',methods=['post'])
def upload():

    # Uploads file
    if request.method == 'POST':
        img = request.files['photo']
        if img:
                filename = secure_filename(img.filename)
                img.save(os.path.join(app.config['IMAGES'], filename))
                s3.upload_file(
                    Bucket = UNPROCESSED_BUCKET_NAME,
                    Filename = os.path.join(app.config['IMAGES'], filename),
                    Key = filename
                )
    
            # Brief Pause, download and display 
                sleep(20)

                edited_file_name = "edited-{}".format(filename)
                s3.download_file( 
                Filename= os.path.join(app.config['IMAGES'], edited_file_name), 
                Bucket=PROCESSED_BUCKET_NAME, 
                Key= edited_file_name)
        sleep(10)
        return render_template("result.html", image_url= os.path.join(app.config['IMAGES'], edited_file_name))

if __name__ == "__main__":
    
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
