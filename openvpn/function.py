import boto3
import requests
import os
import json
import gzip
from base64 import b64encode
from io import BytesIO

s3_client = boto3.client('s3')

# OpenObserve configuration
openobserve_endpoint = os.getenv('OPENOBSERVE_ENDPOINT', 'https://<BASE_URL_O2>/api/default/openvpn/_json')
basic_auth_username = os.getenv('BASIC_AUTH_USERNAME')
basic_auth_password = os.getenv('BASIC_AUTH_PASSWORD')

def lambda_handler(event, context):
    try:
        # Log the entire event for debugging
        print("Received event:", event)
        
        # Check if 'Records' is in the event
        if 'Records' not in event:
            raise ValueError("No 'Records' key found in event")

        # Process each record in the event
        for record in event['Records']:
            # Ensure the event is from SNS
            if 'Sns' not in record:
                raise ValueError("No 'Sns' key found in record")

            # Parse the SNS message
            sns_message = record['Sns']['Message']
            s3_event = json.loads(sns_message)  # Parse the JSON string

            # Process each S3 record in the SNS message
            for s3_record in s3_event.get('Records', []):
                # Ensure the 's3' key is present in the S3 record
                if 's3' not in s3_record:
                    raise ValueError("No 's3' key found in S3 record")

                s3_bucket = s3_record['s3']['bucket']['name']
                s3_key = s3_record['s3']['object']['key']

                # Read logs from S3
                log_lines = read_logs_from_s3(s3_bucket, s3_key)

                # Push logs to OpenObserve
                if log_lines:
                    push_logs_to_openobserve(log_lines)
                else:
                    print("No logs to push.")

    except Exception as e:
        print(f"Error processing event: {e}")

def read_logs_from_s3(bucket, key):
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        compressed_data = response['Body'].read()

        # Decompress the gzipped data
        with gzip.GzipFile(fileobj=BytesIO(compressed_data)) as gz:
            log_data = gz.read().decode('utf-8')
        
        return log_data.splitlines()  # Returns log lines as a list

    except Exception as e:
        print(f"Error reading logs from S3: {e}")
        return []

def push_logs_to_openobserve(log_lines):
    basic_auth_token = b64encode(f"{basic_auth_username}:{basic_auth_password}".encode()).decode()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {basic_auth_token}'
    }
    
    payload = [{"level": "info", "log": line} for line in log_lines]

    try:
        response = requests.post(openobserve_endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            print("Logs successfully pushed to OpenObserve.")
        else:
            print(f"Failed to push logs. Status Code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error pushing logs to OpenObserve: {e}")

