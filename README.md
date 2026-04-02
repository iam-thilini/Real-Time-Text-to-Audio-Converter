# Text to Speech Converter using Amazon Polly
Serverless Text-to-Speech Processing System on AWS

📌 Overview  
This project is a fully serverless text-to-speech conversion system built using AWS managed services. It allows users to upload text files to Amazon S3, automatically processes them with AWS Lambda, converts the text into speech using Amazon Polly, and stores the generated MP3 files in a destination S3 bucket — all without managing servers.

The project demonstrates serverless architecture, event-driven processing, AWS service integration, and cloud best practices for scalability, simplicity, and observability.

---

## 🎯 Problem Statement
Converting written content such as blog posts, notes, or book excerpts into audio usually requires manual tools or tightly coupled applications. These approaches can be:

- Time-consuming
- Hard to scale
- Difficult to automate
- Less flexible for cloud-based workflows

This project solves that problem by providing a cloud-native, serverless pipeline that automatically converts uploaded text files into audio files.

---

## 💡 Solution Summary
A user uploads a `.txt` file into a source S3 bucket.  
That upload triggers an AWS Lambda function via S3 Event Notification.  
The Lambda function reads the text file, sends the content to Amazon Polly, receives the generated audio stream, and uploads the resulting MP3 file into a destination S3 bucket.

This creates a simple, scalable, and fully managed text-to-speech conversion workflow.

---

## 🏗️ Architecture – AWS Services Used

- **Amazon S3** – Stores source text files and generated audio files
- **AWS Lambda** – Serverless processing logic
- **Amazon Polly** – Converts text into speech
- **Amazon CloudWatch** – Logging and monitoring
- **AWS IAM** – Secure role-based access between services

---

## 🔄 Processing Flow

1. User uploads a `.txt` file to the **S3 Source Bucket**
2. **S3 Event Notification** triggers the Lambda function
3. Lambda reads the uploaded text file from S3
4. Lambda sends the text to **Amazon Polly**
5. Amazon Polly converts the text to speech and returns an **AudioStream**
6. Lambda uploads the MP3 file to the **S3 Destination Bucket**
7. End user accesses the generated audio file

---

## 🖼️ Architecture Diagram

![Text to Speech Converter Architecture](./images/architecture.png)

**Figure:** Serverless Text-to-Speech Architecture using Amazon S3, AWS Lambda, and Amazon Polly.

---

## ⚙️ Key Design Decisions

### Serverless-First Architecture
- No servers to provision or maintain
- Automatic scaling based on upload events
- Pay-per-use cost model

### Event-Driven Processing
- File upload in S3 automatically triggers processing
- No manual execution required
- Clean and efficient workflow for document-to-audio conversion

### Decoupled Storage Design
- Separate source and destination buckets
- Clear separation between input text and output audio
- Easier debugging and management

### Environment-Based Configuration
- Bucket names are stored as Lambda environment variables
- No hardcoded configuration in source code
- Easier to reuse across environments

### Observability
- Lambda execution flow is logged in CloudWatch
- Errors and processing stages are easier to trace
- Helps with debugging and reliability

---

## 🧪 How It Works

1. Open the source S3 bucket
2. Upload a `.txt` file
3. S3 automatically triggers the Lambda function
4. Lambda reads the file and sends the text to Amazon Polly
5. Polly generates speech and returns the audio stream
6. Lambda stores the generated `.mp3` file in the destination bucket
7. The final audio file is ready for download or playback

---

## 📘 Detailed Setup Guide
For step-by-step AWS configuration and deployment instructions, see:

👉 [Setup Guide](docs/setup-guide.md)

## 🔐 Security & Reliability
- IAM role-based access is used instead of hardcoded credentials
- Configuration is handled via environment variables
- Managed AWS services provide high availability
- CloudWatch logs help monitor success and troubleshoot failures
- The system uses event-based processing, reducing unnecessary execution

## 🧩 Challenges & Learnings
1️⃣ Understanding Lambda Failure Destinations

**Challenge:**
At first, failed Lambda invocations created unexpected nested files in the destination bucket.

**Learning:**
Those files were not MP3 outputs — they were asynchronous failure records written by Lambda because an **On failure S3 destination** had been configured.

## 2️⃣ Differentiating Polly Output Flow

**Challenge:**
It was initially confusing whether Amazon Polly writes directly to S3.

**Learning:**
When using synthesize_speech, Polly returns an AudioStream to Lambda.
Lambda is responsible for uploading the MP3 file to the destination S3 bucket.

## 3️⃣ Avoiding Hardcoded Bucket Names

**Challenge:**
Using raw bucket names directly in code caused errors and made the function less reusable.

**Learning:**
Storing bucket names in environment variables is cleaner, safer, and aligns with AWS best practices.

## 4️⃣ Planning for Large Text Inputs

**Challenge:**
Synchronous Polly calls are not ideal for large text files.

**Learning:**
For bigger files, a better future improvement is to use Polly S3 Synthesis Tasks instead of AudioStream.

## ✅ Summary
This project showcases:
 - Serverless architecture on AWS
 - Event-driven file processing
 - Text-to-speech conversion using Amazon Polly
 - Integration between S3, Lambda, and Polly
 - CloudWatch-based observability
 - Real-world AWS debugging and configuration experience

It is a simple but practical example of how AWS managed services can be combined to build a scalable media-processing workflow.

🚀 Future Improvements
- Add support for multiple voices
- Add SSML support for pitch, speed, and pronunciation control
- Use Polly S3 Synthesis Tasks for large text files
- Add a frontend for file upload and audio playback
- Notify users when conversion is complete


























