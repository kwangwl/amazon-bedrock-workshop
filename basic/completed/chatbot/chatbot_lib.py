import boto3
import yfinance as yf

# Tool configuration for stock price retrieval
tool_config = {
    "tools": [
        {
            "toolSpec": {
                "name": "get_stock_price",
                "description": "주어진 ticker의 현재 주식 가격을 가져옵니다.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "ticker": {
                                "type": "string",
                                "description": "주식의 ticker"
                            }
                        },
                        "required": [
                            "ticker"
                        ]
                    }
                }
            }
        }
    ]
}

def create_message(role, text):
    return {
        "role": role,
        "content": [{"text": text}]
    }

# Function to retrieve stock price
def get_stock_price(ticker):
    stock_data = yf.Ticker(ticker)
    historical_data = stock_data.history(period='1d')
    date = historical_data.index[0].strftime('%Y-%m-%d')
    current_price = historical_data['Close'].iloc[0]
    return f"{ticker} 종가는 {date} 기준 {current_price:.2f}입니다"

# Function to handle tool use
def handle_tool_use(response):
    if response.get('stopReason') == 'tool_use':
        tool_requests = response['output']['message']['content']
        for tool_request in tool_requests:
            if 'toolUse' in tool_request:
                tool_use = tool_request['toolUse']
                if tool_use['name'] == 'get_stock_price':
                    return get_stock_price(tool_use['input']['ticker'])

# Function to converse with Bedrock model
def converse_with_model(message_history, new_text=None):
    if len(message_history) > 40:
        message_history.clear()
        return True

    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')

    new_message = create_message('user', new_text)
    message_history.append(new_message)

    response = bedrock.converse(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        messages=message_history,
        toolConfig=tool_config,
        inferenceConfig={
            "maxTokens": 2000,
            "temperature": 0,
            "topP": 0.9,
            "stopSequences": []
        },
    )

    tool_response = handle_tool_use(response)
    if tool_response:
        message_history.append({"role": "assistant", "content": [{"text": tool_response}]})
    else:
        output = response['output']['message']['content'][0]['text']
        message_history.append({"role": "assistant", "content": [{"text": output}]})

    return False
