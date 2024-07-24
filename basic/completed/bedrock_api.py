import json
import boto3

# Bedrock client 생성
session = boto3.Session()
bedrock = session.client(service_name='bedrock-runtime')

# 파운데이션 모델 설정
bedrock_model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

# 모델에 보낼 프롬프트
prompt = "대한민국에 섬은 총 몇개인가요?"

# 요청 payload
body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1024,
    "temperature": 0,
    "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
})

# bedrock api 호출
response = bedrock.invoke_model(body=body, modelId=bedrock_model_id)

# 응답 출력
response_body = json.loads(response.get('body').read())
results = response_body.get("content")[0].get("text")
print(results)
