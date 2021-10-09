import requests
import datetime as dt
import smtplib
import os


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
api_key_price = os.environ.get("API_KEY_PRICE")

parameters_price = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_key_price,
}

response = requests.get(url="https://www.alphavantage.co/query", params=parameters_price)
response.raise_for_status()

data = response.json()


daily_data = data["Time Series (Daily)"]
# print(daily_data)

now = dt.datetime.now()
now_year = str(now.year)
now_month = str(now.month)
now_day = str(now.day)

if len(now_month) < 2:
    now_month = "0" + now_month

yesterday = dt.datetime.today() - dt.timedelta(days=1)
yesterday_formatted = yesterday.strftime("%Y-%m-%d")


day_before_yesterday = dt.datetime.today() - dt.timedelta(days=2)
day_before_yesterday_formatted = day_before_yesterday.strftime("%Y-%m-%d")

yesterday_close = float(daily_data[yesterday_formatted]["4. close"])
day_before_yesterday_close = float(daily_data[day_before_yesterday_formatted]["4. close"])


price_difference = yesterday_close - day_before_yesterday_close
percentage_difference = round((abs(price_difference) / day_before_yesterday_close) * 100, 3)

if yesterday_close > day_before_yesterday_close:
    print(f"{STOCK} stock increase {percentage_difference}%")
    subject_msg = f"{STOCK}: Grow {percentage_difference}"
else:
    subject_msg = f"{STOCK}: Lost {percentage_difference}"
    print(f"{STOCK} stock decrease {percentage_difference}%")

api_key_news = os.environ.get("API_KEY_NEWS")
response_news = requests.get(f"https://newsapi.org/v2/top-headlines?q=tesla&from={yesterday}&sortBy=popularity&"
                             f"apiKey={api_key_news}")
response_news.raise_for_status()

news_data = response_news.json()


can_send_email = False

if news_data["totalResults"] != 0:
    first_article_title = news_data["articles"][0]["title"]
    first_article_brief = news_data["articles"][0]["description"]
    first_article = first_article_title + "\n" + first_article_brief
    if news_data["totalResults"] > 1:
        second_article_title = news_data["articles"][1]["title"]
        second_article_brief = news_data["articles"][1]["description"]
        second_article = second_article_title + "\n" + second_article_brief
    else:
        second_article = ""
    can_send_email = True

else:
    print(f"There is no recent articles about {STOCK} :(")


# choose email which you want use to send mails
my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("PASSWORD")

# if percentage_difference >= 5 send email with news
if percentage_difference >= 5 and can_send_email:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs="your_email@gmail.com",
                            msg=f"Subject:{subject_msg}\n\n"
                                f"{first_article}\n\n"
                                f"{second_article}")
