import boto3
import yfinance as yf
import sys

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

def get_response(ticker_symbol):
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime')

    response = bedrock.converse(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',  # 실제 모델 ID로 교체
        messages=[{"role": "user", "content": [{"text": f"{ticker_symbol} 주식의 현재 가격은 얼마입니까?"}]}],
        toolConfig=tool_config
    )
    return response

def get_stock_price(ticker):
    stock_data = yf.Ticker(ticker)
    historical_data = stock_data.history(period='1d')

    date = historical_data.index[0].strftime('%Y-%m-%d')
    current_price = historical_data['Close'].iloc[0]
    return f"{ticker} 종가는 {date} 기준 {current_price:.2f}입니다"

def handle_tool_use(response):
    if response.get('stopReason') == 'tool_use':
        tool_requests = response['output']['message']['content']
        for tool_request in tool_requests:
            if 'toolUse' in tool_request:
                tool_use = tool_request['toolUse']
                print(f"Bedrock Response : {tool_request}")

                if tool_use['name'] == 'get_stock_price':
                    return get_stock_price(tool_use['input']['ticker'])

response = get_response(sys.argv[1])
stock_info = handle_tool_use(response)
print(stock_info)
