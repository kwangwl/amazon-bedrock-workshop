import boto3
import json

def chunk_handler(chunk):
    print(chunk, end='')

def get_streaming_response(prompt, streaming_callback):
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')

    message = {
        "role": "user",
        "content": [{"text": prompt}]
    }

    response = bedrock.converse_stream(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        messages=[message],
        inferenceConfig={
            "maxTokens": 2000,
            "temperature": 0.0
        }
    )

    print("---- Streaming Response ----")
    stream = response.get('stream')
    for event in stream:
        if "contentBlockDelta" in event:
            streaming_callback(event['contentBlockDelta']['delta']['text'])

        if "metadata" in event:
            # Assuming the response contains 'usage' and 'metrics' fields
            print("\n\n---- usage ----")
            print(json.dumps(event['metadata']['usage'], indent=4))

            print("\n---- metrics ----")
            print(json.dumps(event['metadata']['metrics'], indent=4))

prompt = "대한민국에 섬은 총 몇개인가요?"
get_streaming_response(prompt, chunk_handler)
