import yfinance as yf
import io
import boto3


def fetch_and_upload_stock_data(ticker, bucket_name):
    # 주가 정보 가져오기
    data = yf.download(ticker)

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
    fetch_and_upload_stock_data(ticker, bucket_name)
