import boto3
import json
import os
import urllib.parse

polly = boto3.client("polly")
s3 = boto3.client("s3")

# Environment variables
TEXT_BUCKET = os.environ["TEXT_BUCKET"]
AUDIO_BUCKET = os.environ["AUDIO_BUCKET"]

# HARD limit (keep below Polly sync limit)
MAX_CHARS = 2800

def lambda_handler(event, context):
    try:
        record = event["Records"][0]["s3"]
        file_key = urllib.parse.unquote_plus(record["object"]["key"])

        print(f"[START] Processing: s3://{TEXT_BUCKET}/{file_key}")

        # Read text file
        print("[S3] Reading input text")
        obj = s3.get_object(Bucket=TEXT_BUCKET, Key=file_key)
        text = obj["Body"].read().decode("utf-8")

        text_len = len(text)
        print(f"[TEXT] Character count: {text_len}")

        # HARD STOP for large files
        if text_len > MAX_CHARS:
            error_msg = (
                f"Text too large for synchronous Polly call "
                f"({text_len} chars > {MAX_CHARS}). "
                "Use Polly S3 synthesis task."
            )
            print(f"[BLOCKED] {error_msg}")
            raise ValueError(error_msg)

        # Polly conversion
        print("[POLLY] synthesize_speech started")
        polly_response = polly.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId="Joanna"
        )

        if "AudioStream" not in polly_response:
            raise RuntimeError("Polly did not return AudioStream")

        audio_bytes = polly_response["AudioStream"].read()
        print(f"[POLLY] synthesize_speech completed ({len(audio_bytes)} bytes)")

        # Output file name (.txt → .mp3)
        audio_key = (
            file_key[:-4] + ".mp3"
            if file_key.lower().endswith(".txt")
            else file_key + ".mp3"
        )

        print(f"[S3] Uploading MP3 → s3://{AUDIO_BUCKET}/{audio_key}")

        s3.put_object(
            Bucket=AUDIO_BUCKET,
            Key=audio_key,
            Body=audio_bytes,
            ContentType="audio/mpeg"
        )

        print("[SUCCESS] MP3 uploaded successfully")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Text-to-speech conversion successful",
                "source_file": file_key,
                "audio_file": audio_key
            })
        }

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        raise
