import json
import yfinance as yf
from datetime import datetime, timedelta


def get_named_parameter(event, name):
    """
    Lambda 이벤트에서 특정 이름의 파라미터 값을 가져옵니다.
    """
    for param in event['parameters']:
        if param['name'] == name:
            return param['value']
    return None  # 파라미터가 없을 경우 None 반환


def get_stock_chart(ticker):
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=500)

    # 주가 정보 가져오기
    data = yf.download(ticker, start=start_date, end=end_date)
    stock_close = data["Close"]

    prompt = "주식의 날짜별 종가 정보는 다음과 같습니다:\n"
    for index, close in stock_close.items():
        date = index.strftime('%Y-%m-%d')
        prompt += f"{date}:{round(close, 2)}\n"

    return prompt


def get_stock_balance(ticker):
    company = yf.Ticker(ticker)

    # 재무제표 가져와서 최근 3년간의 데이터 선택
    balance = company.balance_sheet
    if balance.shape[1] >= 3:
        balance = balance.iloc[:, :3]
    balance = balance.dropna(how="any")

    prompt = "주식의 날짜별 재무제표 정보는 다음과 같습니다:\n"
    for col in balance.columns:
        date = col.strftime('%Y-%m-%d')
        prompt += f"{date}:\n"
        for item, value in balance[col].items():
            prompt += f"{item}:{value}\n"
    return prompt


def get_recommendations(ticker):
    stock = yf.Ticker(ticker)
    recommendations = stock.recommendations

    prompt = "주식의 시간대별 애널리스트 추천 정도는 다음과 같습니다.:\n"
    for index, row in recommendations.iterrows():
        prompt += (f"{row['period']}: 강력 매수 {row['strongBuy']}건, 매수 {row['buy']}건, 보유 {row['hold']}건,"
                   f" 매도 {row['sell']}건, 강력 매도 {row['strongSell']} 건\n")
    return prompt


def lambda_handler(event, context):
    # get the action group used during the invocation of the lambda function
    actionGroup = event.get('actionGroup', '')

    # name of the function that should be invoked
    function = event.get('function', '')
    ticker = get_named_parameter(event, "ticker")

    if function == 'get_stock_chart':
        prompt = get_stock_chart(ticker)

    elif function == 'get_stock_balance':
        prompt = get_stock_balance(ticker)

    elif function == 'get_recommendations':
        prompt = get_recommendations(ticker)

    else:
        prompt = 'Invalid function'

    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': {'TEXT': {'body': json.dumps(prompt, ensure_ascii=False)}}
        }
    }

    function_response = {'response': action_response, 'messageVersion': event['messageVersion']}
    print("Response: {}".format(function_response))

    return function_response


if __name__ == "__main__":
    # 설정
    event = {
      "function": "get_stock_balance",
      "parameters": [
        {
          "name": "ticker",
          "value": "AAPL"
        }
      ],
      "messageVersion": 4
    }

    # 주가 정보를 가져와 S3에 업로드
    lambda_handler(event, {})
