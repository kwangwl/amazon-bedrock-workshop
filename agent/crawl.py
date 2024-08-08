import requests  # pip install requests
from bs4 import BeautifulSoup  # pip install beautlfulsoup4
import pandas as pd  # pip install pandas

tickers = ['aapl', 'tsla', 'nvda']
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}

for ticker in tickers:
    url = "https://stockanalysis.com/stocks/{0}/forecast/".format(ticker)

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    p_tags = soup.select("p")[:2]

    # 각 <p> 태그 내부의 텍스트 추출
    for p in p_tags:
        print(p.get_text(strip=True))
