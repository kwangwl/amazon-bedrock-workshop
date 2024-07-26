import boto3
import sys


def get_text_response(model):
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')

    message = {
        "role": "user",
        "content": [{"text": "여름에 대해서 묘사해줘"}]
    }

    response = bedrock.converse(
        modelId=model,
        messages=[message],
        inferenceConfig={
            "maxTokens": 2000,
            "temperature": 0,
            "topP": 0.9,
            "stopSequences": []
        },
    )

    return response['output']['message']['content'][0]['text']


response = get_text_response(sys.argv[1])
print(response)
