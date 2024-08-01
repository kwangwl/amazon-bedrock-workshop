import boto3


def create_message(role, text):
    return {
        "role": role,
        "content": [{"text": text}]
    }


def format_messages_for_api(chat_messages):
    messages = []
    for chat_msg in chat_messages:
        messages.append(chat_msg)
    return messages


def converse_with_model(message_history, new_text=None):
    if len(message_history) > 40:
        message_history.clear()
        return True

    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')

    new_message = create_message('user', new_text)
    message_history.append(new_message)

    messages = format_messages_for_api(message_history)
    response = bedrock.converse(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        messages=messages,
        inferenceConfig={
            "maxTokens": 2000,
            "temperature": 0,
            "topP": 0.9,
            "stopSequences": []
        },
    )

    output = response['output']['message']['content'][0]['text']
    response_message = create_message('assistant', output)
    message_history.append(response_message)

    return False
