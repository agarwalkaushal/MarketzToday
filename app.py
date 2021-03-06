import tweepy
import requests
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
import json
import schedule
import time
import urllib.request


def tweet_tweet(text, path):
    print('----------------tweet_tweet------------ start ')
    consumer_key = "AIz32xSHvAE81cdhkJWvWNGLx"
    consumer_secret = "XHDCuCiAJHwEiCoaqvWTBG9R6Kf9cuKpyjvyWjI1ep5P2DKX0k"
    access_key = "1446841040162283526-7yWa67GwRhKHf8Ak5cA6zrc3TI6o9d"
    access_secret = "Lz8tMPuWrV3lxhQ9ZKzXZX6MjOtzhfLb9ToUqq8LkbJUD"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    tweet = text
    image_path = path

    # to attach the media file
    status = api.update_with_media(image_path, tweet)
    try:
        api.update_status(status=status)
    except ValueError:
        print("tweet_tweet exception")
    print('----------------tweet_tweet------------ end ')


def fear_greed_today():
    print('----------------fear_greed_today------------ start ')
    url = "https://fear-and-greed-index.p.rapidapi.com/v1/fgi"
    headers = {
        'x-rapidapi-host': "fear-and-greed-index.p.rapidapi.com",
        'x-rapidapi-key': "ba520daa9cmshd7ba898f17af955p186046jsn44a6770d4b89"
    }
    response = requests.request("GET", url, headers=headers)

    res = json.loads(response.text)
    print(res)
    title = res["fgi"]["now"]["valueText"]
    value = res["fgi"]["now"]["value"]

    if value > 25 and value <= 50:
        color = "darkred"
    elif value > 50 and value <= 75:
        color = "lightgreen"
    elif value > 75 and value <= 100:
        color = "green"
    else:
        color = "yellow"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': color}}))

    fig.update_layout(title="https://twitter.com/MarketzToday", )
    fig.write_image("fig1.png")
    print('----------------fear_greed_today------------ end ')
    tweet_tweet('Equities Fear/Greed today #MarketzToday', 'fig1.png')


def markets_today_us():
    print('----------------markets_today_us------------ start ')
    region = "US"
    url = "https://yfapi.net/v6/finance/quote/marketSummary?lang=en&region="+region
    headers = {'x-api-key': "l7FKFiZ86C7kTcBoszU1c9sAKjeq2uLX4rK0jtuq"}

    response = requests.request("GET", url, headers=headers)

    res = json.loads(response.text)
    print(res)
    sp = res['marketSummaryResponse']['result'][0]
    dji = res['marketSummaryResponse']['result'][1]
    nasdaq = res['marketSummaryResponse']['result'][2]

    data = [sp, dji, nasdaq]

    new = Image.new("RGB", (900, 450))  # , color=(255,255,255,0))
    up = Image.open('up.png')
    down = Image.open('down.png')
    font = ImageFont.truetype("arial.ttf", 32)
    draw = ImageDraw.Draw(new)
    count = 1
    for i in data:
        name = i['shortName']
        current = i['regularMarketPrice']['fmt']
        change = i['regularMarketChange']['fmt']
        change_percent = i['regularMarketChangePercent']['fmt']
        if float(change) >= 0:
            new.paste(up, (150, count*100))
        else:
            new.paste(down, (150, count*100))
        draw.text((200, count*100), name, (255, 255, 255), font=font)
        draw.text((400, count*100), current, (255, 255, 255), font=font)
        draw.text((650, count*100), change_percent, (255, 255, 255), font=font)
        count = count + 1

    font = ImageFont.truetype("arial.ttf", 16)
    draw.text((550, 400), 'https://twitter.com/MarketzToday',
              (255, 255, 255), font=font)
    new.save('fig2.png')
    print('----------------markets_today_us------------ end ')
    tweet_tweet('US market indices today #MarketzToday', 'fig2.png')


def markets_today_in():
    print('----------------markets_today_in------------ start ')
    region = "IN"
    url = "https://yfapi.net/v6/finance/quote/marketSummary?lang=en&region="+region
    headers = {'x-api-key': "l7FKFiZ86C7kTcBoszU1c9sAKjeq2uLX4rK0jtuq"}

    response = requests.request("GET", url, headers=headers)

    res = json.loads(response.text)
    print(res)
    bse = res['marketSummaryResponse']['result'][0]
    nse = res['marketSummaryResponse']['result'][1]

    data = [bse, nse]

    new = Image.new("RGB", (900, 450))  # , color=(255,255,255,0))
    up = Image.open('up.png')
    down = Image.open('down.png')
    font = ImageFont.truetype("arial.ttf", 32)
    draw = ImageDraw.Draw(new)
    count = 1
    for i in data:
        name = i['fullExchangeName']
        current = i['regularMarketPrice']['fmt']
        change = i['regularMarketChange']['fmt']
        change_percent = i['regularMarketChangePercent']['fmt']
        if float(change) >= 0:
            new.paste(up, (150, count*120))
        else:
            new.paste(down, (150, count*120))
        draw.text((200, count*120), name, (255, 255, 255), font=font)
        draw.text((400, count*120), current, (255, 255, 255), font=font)
        draw.text((650, count*120), change_percent, (255, 255, 255), font=font)
        count = count + 1

    font = ImageFont.truetype("arial.ttf", 16)
    draw.text((550, 400), 'https://twitter.com/MarketzToday',
              (255, 255, 255), font=font)
    new.save('fig2.png')
    print('----------------markets_today_in------------ end ')
    tweet_tweet('Indian market indices today #MarketzToday', 'fig2.png')


def bitcoin_today():
    print('----------------bitcoin_today------------ start ')
    urllib.request.urlretrieve(
        "https://alternative.me/crypto/fear-and-greed-index.png", "fig3.png")
    print('----------------bitcoin_today------------ end ')
    tweet_tweet('Bitcoin Fear/Greed today #MarketzToday', 'fig3.png')


schedule.every().day.at("00:00").do(bitcoin_today)

schedule.every().monday.at("10:30").do(markets_today_in)
schedule.every().monday.at("13:00").do(fear_greed_today)
schedule.every().monday.at("20:30").do(markets_today_us)

schedule.every().tuesday.at("10:30").do(markets_today_in)
schedule.every().tuesday.at("13:00").do(fear_greed_today)
schedule.every().tuesday.at("20:30").do(markets_today_us)

schedule.every().wednesday.at("10:30").do(markets_today_in)
schedule.every().wednesday.at("13:00").do(fear_greed_today)
schedule.every().wednesday.at("20:30").do(markets_today_us)

schedule.every().thursday.at("10:30").do(markets_today_in)
schedule.every().thursday.at("13:00").do(fear_greed_today)
schedule.every().thursday.at("20:30").do(markets_today_us)

schedule.every().friday.at("10:30").do(markets_today_in)
schedule.every().friday.at("13:00").do(fear_greed_today)
schedule.every().friday.at("20:30").do(markets_today_us)

while 1:
    print('running')
    schedule.run_pending()
    time.sleep(1)
