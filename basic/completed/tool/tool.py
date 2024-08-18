import boto3
import yfinance as yf

# AWS Bedrock 클라이언트 생성
session = boto3.Session()
bedrock = session.client(service_name='bedrock-runtime')
tool_config = {
    "tools": [
        {
            "toolSpec": {
                "name": "get_stock_price",
                "description": "Fetches the current stock price for a given ticker symbol.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "ticker": {
                                "type": "string",
                                "description": "Ticker symbol of the stock."
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


# Converse API 호출
def call_converse_api(ticker_symbol):
    response = bedrock.converse(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',  # 실제 모델 ID로 교체
        messages=[{"role": "user", "content": [{"text": f"What is the current price of {ticker_symbol} stock?"}]}],
        toolConfig=tool_config
    )
    return response


def get_stock_price(ticker):
    stock_data = yf.Ticker(ticker)
    historical_data = stock_data.history(period='1d')

    date = historical_data.index[0].strftime('%Y-%m-%d')
    current_price = historical_data['Close'].iloc[0]
    return f"{date}의 {ticker} 종가는 {current_price:.2f}입니다"


# yfinance를 사용한 도구 호출 및 결과 처리
def handle_tool_use(response):
    if response.get('stopReason') == 'tool_use':
        tool_requests = response['output']['message']['content']

        for tool_request in tool_requests:
            if 'toolUse' in tool_request:
                tool_use = tool_request['toolUse']
                if tool_use['name'] == 'get_stock_price':
                    ticker = tool_use['input']['ticker']
                    return get_stock_price(ticker)

# 예시 호출
response = call_converse_api("AAPL")
stock_info = handle_tool_use(response)
print(stock_info)
