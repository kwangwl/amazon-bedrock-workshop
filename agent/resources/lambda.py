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
    data = data["Close"]

    # data_dict = {date.strftime('%Y-%m-%d'): round(value, 2) for date, value in data.items()}
    return data.to_json()


def get_stock_balance(ticker):
    # yfinance를 사용하여 주식 티커에 해당하는 회사 정보 가져오기
    company = yf.Ticker(ticker)

    # 대차대조표 가져오기
    balance_sheet = company.balance_sheet

    # 대차대조표에서 최근 3년간의 데이터 선택
    if balance_sheet.shape[1] >= 3:
        balance_sheet = balance_sheet.iloc[:, :3]  # 최근 3년간의 데이터만 선택

    # 결측값이 있는 행 제거
    balance_sheet = balance_sheet.dropna(how="any")

    # output 정제
    balance_sheet_dict = {}
    for date, value in balance_sheet.items():
        balance_sheet_dict.update({date.strftime('%Y-%m-%d'): {key: int(item) for key, item in value.items()}})

    return balance_sheet_dict


def lambda_handler(event, context):
    # get the action group used during the invocation of the lambda function
    actionGroup = event.get('actionGroup', '')

    # name of the function that should be invoked
    function = event.get('function', '')

    if function == 'get_stock_chart':
        # 예시로 사용할 주식 티커
        ticker = get_named_parameter(event, "ticker")
        output = get_stock_chart(ticker)
        responseBody = {'TEXT': {'body': json.dumps(output)}}

    elif function == 'get_stock_balance':
        # 예시로 사용할 주식 티커
        ticker = get_named_parameter(event, "ticker")
        output = get_stock_balance(ticker)
        responseBody = {'TEXT': {'body': json.dumps(output)}}

    else:
        responseBody = {'TEXT': {'body': 'Invalid function'}}

    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }
    }

    function_response = {'response': action_response, 'messageVersion': event['messageVersion']}
    print("Response: {}".format(function_response))

    return function_response


if __name__ == "__main__":
    msft = yf.Ticker("MSFT")

    # 설정
    event = {
      "function": "get_stock_chart",
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
