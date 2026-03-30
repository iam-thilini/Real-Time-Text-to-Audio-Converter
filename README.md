# Real Time Text to Audio Converter
A serverless Text-to-Speech (TTS) conversion system built on AWS.
This project automatically converts uploaded text files into natural-sounding speech using Amazon Polly.
Users upload a .txt file to an Amazon S3 bucket, and the system generates an MP3 audio file without managing any servers.
Voice parameters such as voice type, pitch, and speech rate can be customized within the Lambda function.

## Architecture Overview
**Workflow:**
1. A text file (.txt) is uploaded to an Amazon S3 bucket
2. An S3 event triggers an AWS Lambda function
3. The Lambda function reads the text file
4. Amazon Polly converts the text into speech
5. The generated MP3 file is stored in a destination S3 bucket

##AWS Services Used
- **Amazon S3** – Source and destination storage for text and audio files
- **AWS Lambda** – Serverless text-to-speech processing logic
- **Amazon Polly** – Text-to-Speech conversion service
- **AWS IAM** – Secure role-based access for AWS services
- **Amazon CloudWatch** – Logging and monitoring

## Step-by-Step Setup Guide
### 1️⃣ Create IAM Role for Lambda
Create an IAM role that allows Lambda to access Polly and S3.

1. Open IAM → Roles → Create role
2. Trusted entity:
    - AWS service
    - Use case: Lambda
3. Attach the following policies:
    - AmazonPollyFullAccess
    - AmazonS3FullAccess
    - AWSLambdaBasicExecutionRole
4. Role name:
  ```
  PollyTranslationRole
  ```
5. Create the role

### 2️⃣ Create S3 Buckets
Create two S3 buckets.
1. Source Bucket (Text Files)
  - Example name:
  ```
  th-polly-text-files-storage-bucket
  ```
  - This bucket will store uploaded `.txt` files
2. Destination Bucket (Audio Files)
  - Example name:
  ```
  th-polly-audio-files-storage-bucket
  ```
This bucket will store generated `.mp3` files

Keep all other settings as **default**.





















