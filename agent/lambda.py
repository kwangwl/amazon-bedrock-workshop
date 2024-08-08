import json
import uuid
import boto3
import io
import csv
import requests
from bs4 import BeautifulSoup

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('restaurant_bookings')


def get_stock_chart(ticker):
    bucket_name = 'agent-test-kw'
    file_key = f"{ticker.upper()}.csv"

    # S3에서 파일 가져오기
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    content = response['Body'].read().decode('utf-8')

    # CSV 파일을 pandas DataFrame으로 읽기
    csv_reader = csv.DictReader(io.StringIO(content))
    json_data = json.dumps([row for row in csv_reader])

    return json_data


def get_analyst_report(ticker):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}
    url = f"https://stockanalysis.com/stocks/{ticker}/forecast/"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    p_tags = soup.select("p")[:2]

    # 각 <p> 태그 내부의 텍스트 추출
    return [p.get_text(strip=True) for p in p_tags]


def get_named_parameter(event, name):
    """
    Lambda 이벤트에서 특정 이름의 파라미터 값을 가져옵니다.
    """
    for param in event['parameters']:
        if param['name'] == name:
            return param['value']
    return None  # 파라미터가 없을 경우 None 반환


def get_booking_details(booking_id):
    """
    Retrieve details of a restaurant booking

    Args:
        booking_id (string): The ID of the booking to retrieve
    """
    try:
        response = table.get_item(Key={'booking_id': booking_id})
        if 'Item' in response:
            return response['Item']
        else:
            return {'message': f'No booking found with ID {booking_id}'}
    except Exception as e:
        return {'error': str(e)}


def create_booking(date, name, hour, num_guests):
    """
    Create a new restaurant booking

    Args:
        date (string): The date of the booking
        name (string): Name to idenfity your reservation
        hour (string): The hour of the booking
        num_guests (integer): The number of guests for the booking
    """
    try:
        booking_id = str(uuid.uuid4())[:8]
        table.put_item(
            Item={
                'booking_id': booking_id,
                'date': date,
                'name': name,
                'hour': hour,
                'num_guests': num_guests
            }
        )
        return {'booking_id': booking_id}
    except Exception as e:
        return {'error': str(e)}


def delete_booking(booking_id):
    """
    Delete an existing restaurant booking

    Args:
        booking_id (str): The ID of the booking to delete
    """
    try:
        response = table.delete_item(Key={'booking_id': booking_id})
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {'message': f'Booking with ID {booking_id} deleted successfully'}
        else:
            return {'message': f'Failed to delete booking with ID {booking_id}'}
    except Exception as e:
        return {'error': str(e)}


def lambda_handler(event, context):
    # get the action group used during the invocation of the lambda function
    actionGroup = event.get('actionGroup', '')

    # name of the function that should be invoked
    function = event.get('function', '')

    # parameters to invoke function with
    parameters = event.get('parameters', [])

    if function == 'get_booking_details':
        booking_id = get_named_parameter(event, "booking_id")
        if booking_id:
            response = str(get_booking_details(booking_id))
            responseBody = {'TEXT': {'body': json.dumps(response)}}
        else:
            responseBody = {'TEXT': {'body': 'Missing booking_id parameter'}}

    elif function == 'create_booking':
        date = get_named_parameter(event, "date")
        name = get_named_parameter(event, "name")
        hour = get_named_parameter(event, "hour")
        num_guests = get_named_parameter(event, "num_guests")

        if date and hour and num_guests:
            response = str(create_booking(date, name, hour, num_guests))
            responseBody = {'TEXT': {'body': json.dumps(response)}}
        else:
            responseBody = {'TEXT': {'body': 'Missing required parameters'}}

    elif function == 'delete_booking':
        booking_id = get_named_parameter(event, "booking_id")
        if booking_id:
            response = str(delete_booking(booking_id))
            responseBody = {'TEXT': {'body': json.dumps(response)}}
        else:
            responseBody = {'TEXT': {'body': 'Missing booking_id parameter'}}

    elif function == 'get_stock_chart':
        # 예시로 사용할 주식 티커
        ticker = get_named_parameter(event, "ticker")
        hist = get_stock_chart(ticker)
        responseBody = {'TEXT': {'body': hist}}

    elif function == 'get_analyst_report':
        # 예시로 사용할 주식 티커
        ticker = get_named_parameter(event, "ticker")
        hist = get_analyst_report(ticker)
        responseBody = {'TEXT': {'body': hist}}

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