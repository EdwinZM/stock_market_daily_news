import requests
import os
import datetime
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

API_KEY = os.environ.get("API_KEY")
news_key = os.environ.get("news_key")
account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": API_KEY
}
response = requests.get(STOCK_ENDPOINT, params=params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]

now = datetime.datetime.now()
year = now.year
month = now.month
yesterday = now.day - 1

if month < 10:
    month = f"0{month}"

yesterday_data = data[f"{year}-{month}-{yesterday}"]
day_before = data[f"{year}-{month}-{yesterday - 1}"]

yesterday_stock = float(yesterday_data["4. close"])
day_before_stock = float(day_before["4. close"])

if yesterday_stock >= day_before_stock + day_before_stock * .5 or yesterday_stock <= day_before_stock + day_before_stock * .5:
    news_params = {
        "q": COMPANY_NAME,
        "sortBy": "publishedAt",
        "apiKey": news_key
    }

    response = requests.get(NEWS_ENDPOINT, params=news_params)
    data = response.json()["articles"]
    news = [data[i] for i in range(3)]
    
    client = Client(account_sid, auth_token)

    for data in news:
        title = data["title"]
        description = data["description"]
        url = data["url"]
        print(f"{title}\n{description}\n{url}")
        message = client.messages \
                        .create(
                            body=f"{title}\n\n{description}\n{url}",
                            from_='+18329811002',
                            to='+529981613497'
                        )

  






