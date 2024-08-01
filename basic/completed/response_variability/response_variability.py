import boto3
import sys


def get_text_response(input_content, model_id, temperature):
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')

    message = {
        "role": "user",
        "content": [{"text": input_content}]
    }

    response = bedrock.converse(
        modelId=model_id,
        messages=[message],
        inferenceConfig={
            "maxTokens": 2000,
            "temperature": temperature,
            "topP": 0.9,
            "stopSequences": []
        },
    )

    return response['output']['message']['content'][0]['text']


prompt = "생성형 AI에 대해 한줄로 설명해줘"
for i in range(3):
    response = get_text_response(prompt, sys.argv[1], float(sys.argv[2]))
    print(response, end='\n\n')
