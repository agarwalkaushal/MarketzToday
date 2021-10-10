import tweepy
import requests
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
import json
import schedule
import time


def tweet_tweet(text, path):
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
    api.update_status(status=status)


def fear_greed_today():

    url = "https://fear-and-greed-index.p.rapidapi.com/v1/fgi"
    headers = {
        'x-rapidapi-host': "fear-and-greed-index.p.rapidapi.com",
        'x-rapidapi-key': "ba520daa9cmshd7ba898f17af955p186046jsn44a6770d4b89"
    }
    response = requests.request("GET", url, headers=headers)

    res = json.loads(response.text)

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
    tweet_tweet('Fear/Greed today #MarketzToday', 'fig1.png')


def markets_today():

    region = "US"
    url = "https://yfapi.net/v6/finance/quote/marketSummary?lang=en&region="+region
    headers = {'x-api-key': "l7FKFiZ86C7kTcBoszU1c9sAKjeq2uLX4rK0jtuq"}

    response = requests.request("GET", url, headers=headers)

    res = json.loads(response.text)

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
    tweet_tweet('Market indices today #MarketzToday', 'fig2.png')


schedule.every().monday.at("09:00").do(fear_greed_today)
schedule.every().monday.at("16:30").do(markets_today)
schedule.every().tuesday.at("09:00").do(fear_greed_today)
schedule.every().tuesday.at("16:30").do(markets_today)
schedule.every().wednesday.at("09:00").do(fear_greed_today)
schedule.every().wednesday.at("16:30").do(markets_today)
schedule.every().thursday.at("09:00").do(fear_greed_today)
schedule.every().thursday.at("16:30").do(markets_today)
schedule.every().friday.at("09:00").do(fear_greed_today)
schedule.every().friday.at("16:30").do(markets_today)

while 1:
    schedule.run_pending()
    time.sleep(1)
