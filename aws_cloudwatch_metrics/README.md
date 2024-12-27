
# CloudFormation Template for Streaming CloudWatch Metrics to OpenObserve via Kinesis Firehose

This repository contains an AWS CloudFormation template to set up a pipeline for streaming CloudWatch Metrics to OpenObserve using Kinesis Firehose. The template automates the creation of required AWS resources, such as roles, Firehose delivery streams, and CloudWatch metric streams.

---

## Features

- **CloudWatch Metric Stream**: Captures CloudWatch metrics and forwards them to Kinesis Firehose.
- **Kinesis Firehose Delivery Stream**: Streams metrics to an HTTP endpoint for ingestion into OpenObserve.
- **S3 Backup**: Provides a backup mechanism for failed deliveries in a specified S3 bucket.
- **IAM Roles**: Secure role-based access controls for both CloudWatch Metric Stream and Kinesis Firehose.

---

## Prerequisites

Before deploying the template, ensure you have:

1. **AWS Account**: An active AWS account with sufficient permissions to create the necessary resources.
2. **S3 Bucket**: An existing S3 bucket for backup storage.
3. **Active OpenObserve**: The HTTP endpoint URL, name, and access key for integration with OpenObserve.

---

## Parameters

| Parameter Name      | Description                                                    | Type   |
|---------------------|----------------------------------------------------------------|--------|
| `HttpEndpointName`  | Name of the OpenObserve endpoint for Kinesis Firehose.         | String |
| `AccessKey`         | Access key for authentication with the O2 endpoint.         | String |
| `HttpEndpointUrl`   | URL of the O2 endpoint for Kinesis Firehose.                | String |
| `S3BackupBucket`    | Name of the S3 bucket for Firehose backup.                    | String |

---

## Resources Created

1. **CloudWatch Metric Stream**:
   - Captures metrics from AWS services and streams them to Kinesis Firehose.
   - Supports OpenTelemetry 1.0 output format.

2. **Kinesis Firehose Delivery Stream**:
   - Streams metrics to the specified HTTP endpoint.
   - Includes buffering and retry mechanisms for reliability.
   - Configured to log failed deliveries in the S3 backup bucket.

3. **IAM Roles**:
   - `MetricsStreamRole`: Grants CloudWatch Metric Stream permission to write to Kinesis Firehose.
   - `FirehoseRole`: Grants Kinesis Firehose access to the S3 bucket and CloudWatch logs.

4. **S3 Backup**:
   - Stores failed delivery data for further analysis or recovery.

---

## Deployment Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

2. Deploy the CloudFormation stack:
   ```bash
   aws cloudformation deploy \
     --template-file template.yaml \
     --stack-name OpenObserveMetricsPipeline \
     --parameter-overrides \
       HttpEndpointName=<YourHttpEndpointName> \
       AccessKey=<YourAccessKey> \
       HttpEndpointUrl=<YourHttpEndpointUrl> \
       S3BackupBucket=<YourS3BucketName> \
     --capabilities CAPABILITY_NAMED_IAM
   ```

3. Verify the deployment:
   - Navigate to the AWS Management Console.
   - Check the created resources under **CloudWatch**, **Kinesis Firehose**, and **IAM Roles**.

---

## Outputs

| Output Name            | Description                                |
|------------------------|--------------------------------------------|
| `MetricsStreamName`    | Name of the CloudWatch Metric Stream.      |
| `KinesisFirehoseName`  | Name of the Kinesis Firehose.              |
| `BackupBucketName`     | Name of the backup bucket being used.      |

---

## Cleanup

To delete the stack and associated resources, run:
```bash
aws cloudformation delete-stack --stack-name OpenObserveMetricsPipeline
```