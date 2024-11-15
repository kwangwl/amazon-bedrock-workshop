import boto3

def get_streaming_response(prompt_input, transcription_text, response_placeholder, language='ko'):
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')

    transcript_instruction = {
        'ko': "<transcript> 에는 상담원과 고객간의 통화 녹취가 기록되어 있습니다. 이 녹취를 바탕으로 답변해주세요.",
        'en': "<transcript> contains the call transcript between the agent and the customer. Please answer based on this transcript."
    }

    message = {
        "role": "user",
        "content": [
            {"text": f"<transcript>{transcription_text}</transcript>"},
            {"text": transcript_instruction[language]},
            {"text": prompt_input}
        ]
    }

    response = bedrock.converse_stream(
        modelId='anthropic.claude-3-5-sonnet-20240620-v1:0',
        messages=[message],
        inferenceConfig={
            "maxTokens": 2000,
            "temperature": 0.0
        }
    )

    stream = response.get('stream')
    response_text = ""
    for event in stream:
        if "contentBlockDelta" in event:
            response_text += event['contentBlockDelta']['delta']['text']
            response_placeholder.write(response_text)