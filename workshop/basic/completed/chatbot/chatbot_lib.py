import boto3
import yfinance as yf

tool_config = {
    "tools": [
        {
            "toolSpec": {
                "name": "get_stock_price",
                "description": "현재 주식 가격을 가져옵니다.",
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

def get_stock_price(ticker):
    stock_data = yf.Ticker(ticker)
    historical_data = stock_data.history(period='1d')
    date = historical_data.index[0].strftime('%Y-%m-%d')
    current_price = historical_data['Close'].iloc[0]
    return f"{ticker} 종가는 {date} 기준 {current_price:.2f}입니다"

# Function to converse with Bedrock model
def get_response(message_history):
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')

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

    return response

def handle_response(response):
    output = None

    if response.get('stopReason') == 'tool_use':
        tool_requests = response['output']['message']['content']
        for tool_request in tool_requests:
            if 'toolUse' in tool_request:
                tool_use = tool_request['toolUse']
                if tool_use['name'] == 'get_stock_price':
                    output = get_stock_price(tool_use['input']['ticker'])
    else:
        output = response['output']['message']['content'][0]['text']

    return output
