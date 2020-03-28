#!/usr/bin/python
import logging
import urllib.request
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def download_data(url, file_name):
    urllib.request.urlretrieve(url, '/tmp/' + file_name)


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def lambda_handler(event, context):
    # Entry point for Lambda Execution
    download_data('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv', 'us-counties.csv')
    download_data('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv', 'us-states.csv')
    upload_file('/tmp/us-states.csv', 'mybigdatabucket', 'covid19/nyt/states/us-states.csv')
    upload_file('/tmp/us-counties', 'mybigdatabucket', 'covid19/nyt/counties/us-counties.csv')


if __name__ == '__main__':
    # Entry point for local testing
    lambda_handler('', '')
