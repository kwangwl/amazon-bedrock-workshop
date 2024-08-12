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
    today = datetime.today().date()
    start_date = today - timedelta(days=500)

    # 주가 정보 가져오기
    data = yf.download(ticker, start=start_date, end=today)
    stock_close = data["Close"]

    output = {}
    for index, close in stock_close.items():
        output.update({
            index.strftime('%Y-%m-%d'): round(close, 2)
        })

    return output


def get_stock_balance(ticker):
    company = yf.Ticker(ticker)

    # 재무제표 가져와서 최근 3년간의 데이터 선택
    balance = company.balance_sheet
    if balance.shape[1] >= 3:
        balance = balance.iloc[:, :3]
    balance = balance.dropna(how="any")

    output = {}
    for col in balance.columns:
        output_date = {}
        for item, value in balance[col].items():
            output_date.update({
                item: value
            })
        output.update({col.strftime('%Y-%m-%d'): output_date})
    return output

def get_recommendations(ticker):
    stock = yf.Ticker(ticker)
    recommendations = stock.recommendations

    output = {}
    for index, row in recommendations.iterrows():
        output.update({
            row['period'] : {
                'strongBuy': row['strongBuy'],
                'buy': row['buy'],
                'hold': row['hold'],
                'sell': row['sell'],
                'strongSell': row['strongSell'],

            }
        })
    return output


def get_today():
    today = datetime.today().date()
    return today.strftime('%Y-%m-%d')


def lambda_handler(event, context):
    # get the action group used during the invocation of the lambda function
    actionGroup = event.get('actionGroup', '')

    # name of the function that should be invoked
    function = event.get('function', '')

    if function == 'get_today':
        output = get_today()

    elif function == 'get_stock_chart':
        ticker = get_named_parameter(event, "ticker")
        output = get_stock_chart(ticker)

    elif function == 'get_stock_balance':
        ticker = get_named_parameter(event, "ticker")
        output = get_stock_balance(ticker)

    elif function == 'get_recommendations':
        ticker = get_named_parameter(event, "ticker")
        output = get_recommendations(ticker)

    else:
        output = 'Invalid function'

    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': {'TEXT': {'body': json.dumps(output)}}
        }
    }

    function_response = {'response': action_response, 'messageVersion': event['messageVersion']}
    print("Response: {}".format(function_response))

    return function_response

