import boto3
import json

session = boto3.Session()
bedrock = session.client(service_name='bedrock-runtime')

model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
message = {
    "role": "user",
    "content": [
        {"text": "대한민국에 섬은 총 몇개인가요?"}
    ],
}

response = bedrock.converse(
    modelId=model_id,
    messages=[message],
    inferenceConfig={
        "maxTokens": 2000,
        "temperature": 0
    },
)

print("\n---- output ----")
print(json.dumps(response["output"], indent=4, ensure_ascii=False))

print("\n---- usage ----")
print(json.dumps(response['usage'], indent=4))

print("\n---- metrics ----")
print(json.dumps(response['metrics'], indent=4))
