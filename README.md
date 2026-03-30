# Real Time Text to Audio Converter
A serverless Text-to-Speech (TTS) conversion system built on AWS.
This project automatically converts uploaded text files into natural-sounding speech using **Amazon Polly**.
Users upload a .txt file to an Amazon S3 bucket, and the system generates an MP3 audio file without managing any servers.
Voice parameters such as voice type, pitch, and speech rate can be customized within the Lambda function.

## Architecture Overview
**Workflow:**
1. A text file (.txt) is uploaded to an Amazon S3 bucket
2. An S3 event triggers an AWS Lambda function
3. The Lambda function reads the text file
4. Amazon Polly converts the text into speech
5. The generated MP3 file is stored in a destination S3 bucket

## AWS Services Used
- **Amazon S3** – Source and destination storage for text and audio files
- **AWS Lambda** – Serverless text-to-speech processing logic
- **Amazon Polly** – Text-to-Speech conversion service
- **AWS IAM** – Secure role-based access for AWS services
- **Amazon CloudWatch** – Logging and monitoring

## Step-by-Step Setup Guide
### 1️⃣ Create IAM Role for Lambda
Create an IAM role that allows Lambda to access Polly and S3.

1. Open **IAM** → Roles → Create role
2. Trusted entity:
    - **AWS service**
    - Use case: **Lambda**
4. Attach the following policies:
    - AmazonPollyFullAccess
    - AmazonS3FullAccess
    - AWSLambdaBasicExecutionRole
5. Role name:
  ```
  PollyTranslationRole
  ```
5. Create the role

### 2️⃣ Create S3 Buckets
Create **two S3 buckets**.
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

## 3️⃣ Create the Lambda Function
1. Open **AWS Lambda** → Create function
2. Select **Author from scratch**

**Function settings:**
- Function name:
```
PollyTranslationFunction
```
- Runtime:
```
Python 3.14
```
- Execution role:
    - Use an existing role
    - Select:
      ```
      PollyTranslationRole
      ```
3. Create the function

## 4️⃣ Configure Lambda Environment Variables
Go to **Configuration → Environment variables** and add:

| Key          | Value                               |
| ------------ | ----------------------------------- |
| TEXT_BUCKET  | th-polly-text-files-storage-bucket  |
| AUDIO_BUCKET | th-polly-audio-files-storage-bucket |

These variables define the source and destination S3 buckets.

## 5️⃣ Add Lambda Code
1. Open the **Code** tab
2. Replace the default code with your **Text-to-Speech Lambda function code**
3. Click **Deploy**

The Lambda function:
 - Reads text from the source S3 bucket
 - Converts it to speech using Amazon Polly
 - Uploads the generated MP3 to the destination bucket

## 6️⃣ Configure S3 Trigger
1. Open the **source S3 bucket**
2. Go to **Properties**
3. Scroll to **Event notifications**
4. Click **Create event notification**

**Event configuration:**
 - Name:
   ```
    TextUploadTrigger
   ```
 - Event types:
    - ✅ Object created (PUT)
 - Suffix:
   ```
    .txt
   ```
 - Destination:
    - Lambda function
    - Select:
      ```
        PollyTranslationFunction
      ```
 - Enable:
    - ✅ Recursive invocation

Save the configuration.

## 7️⃣ Configure Lambda Destination (Failure Handling)

To capture failed invocations:
1. Open **Lambda → PollyTranslationFunction**
2. Go to **Configuration → Asynchronous invocation**
3. Add a destination:

Settings:
 - Condition:
   ```
    On failure
   ```
 - Destination type:
   ```
    S3 bucket
   ```
 - Destination:
   ```
    th-polly-audio-files-storage-bucket
   ```
This stores failure records in S3 for debugging and auditing.





























