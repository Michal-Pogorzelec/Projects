import requests
from bs4 import BeautifulSoup
import lxml
from smtplib import SMTP
import os

URL = "https://www.amazon.pl/Apple-iPhone-12-Pro-128-GB/dp/B08TC39QLF/ref=sr_1_7?__mk_pl_PL=ÅMÅŽÕÑ&dchild=1&keywords=iphone&qid=1633372980&sr=8-7&th=1"

header = {
    "User-Agent": os.environ.get("user_agent"),
    "Accept-Language": os.environ.get("language"),
}

response = requests.get(url=URL, headers=header)

html_website = response.content


soup = BeautifulSoup(html_website, "lxml")

price = soup.find("span", id="priceblock_ourprice").getText()

price = price.split()
price = float(price[0] + price[1].split(",")[0])

# using the environment variables
my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("PASSWORD")
max_price = 4500.0

if price < max_price:
    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs="michalpogorzelec10@gmail.com",
                            msg="Subject: Price Alert\n\n"
                                f"Your product is now less than {max_price}.")
