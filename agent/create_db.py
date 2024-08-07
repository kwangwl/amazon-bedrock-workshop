import yfinance as yf
import io
import boto3
from datetime import datetime, timedelta


def fetch_and_upload_financial_statements(ticker, bucket_name):
    # 티커에 점(.)이 포함되어 있는 경우, 점 이전의 부분만 사용
    if "." in ticker:
        ticker = ticker.split(".")[0]

    # yfinance를 사용하여 주식 티커에 해당하는 회사 정보 가져오기
    company = yf.Ticker(ticker)

    # 대차대조표 가져오기
    balance_sheet = company.balance_sheet

    # 대차대조표에서 최근 3년간의 데이터 선택
    if balance_sheet.shape[1] >= 3:
        balance_sheet = balance_sheet.iloc[:, :3]  # 최근 3년간의 데이터만 선택

    # 결측값이 있는 행 제거
    balance_sheet = balance_sheet.dropna(how="any")

    # 대차대조표를 CSV 형식으로 변환
    csv_buffer = io.StringIO()
    balance_sheet.to_csv(csv_buffer)

    # S3에 업로드
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Body=csv_buffer.getvalue(), Key=f"{ticker}_balance_sheet.csv")

def fetch_and_upload_stock_data(ticker, bucket_name):
    # 오늘 날짜와 500일 전 날짜 계산
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=700)

    # 주가 정보 가져오기
    data = yf.download(ticker, start=start_date, end=end_date)

    # CSV 파일로 저장
    csv_buffer = io.StringIO()
    data.to_csv(csv_buffer)

    # S3에 업로드
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Body=csv_buffer.getvalue(), Key=f"{ticker}.csv")


if __name__ == "__main__":
    # 설정
    ticker = 'AAPL'
    bucket_name = 'agent-test-kw'

    # 주가 정보를 가져와 S3에 업로드
    # fetch_and_upload_stock_data(ticker, bucket_name)
    fetch_and_upload_financial_statements(ticker, bucket_name)
