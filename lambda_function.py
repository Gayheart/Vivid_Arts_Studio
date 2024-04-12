import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image
import PIL.Image
            
s3_client = boto3.client('s3')
            
def black_white(image_path, edited_path):
  with Image.open(image_path) as image:
    image = image.convert("L")
    image.save(edited_path)
            
def lambda_handler(event, context):
  for record in event['Records']:
    bucket = record['s3']['bucket']['name']
    key = unquote_plus(record['s3']['object']['key'])
    tmpkey = key.replace('/', '')
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
    upload_path = '/tmp/edited-{}'.format(tmpkey)
    s3_client.download_file(bucket, key, download_path)
    black_white(download_path, upload_path)
    s3_client.upload_file(upload_path, 'vivid-arts-processed', 'edited-{}'.format(key))