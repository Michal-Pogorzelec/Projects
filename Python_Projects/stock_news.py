import requests
import datetime as dt

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
api_key_price = "RH1S2W39OHVFQ7Q6"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
parameters_price = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_key_price,
}

response = requests.get(url="https://www.alphavantage.co/query", params=parameters_price)
response.raise_for_status()
# print(response)
data = response.json()
# print(data)

daily_data = data["Time Series (Daily)"]
print(daily_data)

now = dt.datetime.now()
now_year = str(now.year)
now_month = str(now.month)
now_day = str(now.day)

if len(now_month) < 2:
    now_month = "0" + now_month
# yesterday = now - dt.timedelta(days=1)
# yesterday = now_year + "-" + now_month + "-" + str(int(now_day) - 1)
# Skrócona wersja formatowania daty, tylko jak dać poprzedni dzien lub 2 dni temu?
yesterday = dt.datetime.today() - dt.timedelta(days=1)
yesterday_formatted = yesterday.strftime("%Y-%m-%d")

# TODO:1 Under this line
# What will happen with day_before_yesterday when yesterday's day would be 1st ???

day_before_yesterday = dt.datetime.today() - dt.timedelta(days=2)
day_before_yesterday_formatted = day_before_yesterday.strftime("%Y-%m-%d")

yesterday_close = float(daily_data[yesterday_formatted]["4. close"])
day_before_yesterday_close = float(daily_data[day_before_yesterday_formatted]["4. close"])
# print(yesterday_close)
# print(day_before_yesterday_close)

price_difference = yesterday_close - day_before_yesterday_close
percentage_difference = round((abs(price_difference) / day_before_yesterday_close) * 100, 3)

if yesterday_close > day_before_yesterday_close:
    print(f"{STOCK} stock increase {percentage_difference}%")
    subject_msg = f"{STOCK}: Grow {percentage_difference}"
else:
    subject_msg = f"{STOCK}: Lost {percentage_difference}"
    print(f"{STOCK} stock decrease {percentage_difference}%")


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
# api_key_news = "c884958d8b2342788fd8be24605033f4"

response_news = requests.get(f"https://newsapi.org/v2/top-headlines?q=tesla&from={yesterday}&sortBy=popularity&"
                             f"apiKey=c884958d8b2342788fd8be24605033f4")
response_news.raise_for_status()

news_data = response_news.json()
# print(news_data)

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

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
import smtplib

# choose email which you want use to send mails
my_email = "sending_email@gmail.com"
password = "password"

if percentage_difference >= 1 and can_send_email:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs="your_email10@gmail.com",
                            msg=f"Subject:{subject_msg}\n\n"
                                f"{first_article}\n\n"
                                f"{second_article}")
