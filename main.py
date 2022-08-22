from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['2020.03.06']
city = os.environ['合肥']
birthday = os.environ['2022.11.08']

app_id = os.environ["wx47ba38e8c92bcc4a"]
app_secret = os.environ["fa72cf3796a457b236a7c8b9ecc5990f"]

user_id = os.environ["oYLqg6mB5y0nm7uG4F1YWtcGwTUM"]
template_id = os.environ["B-s_R0hcRePTio8pZzxKaj7VQY5OrRwQBD_zmyy1oLQ"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=oYLqg6mB5y0nm7uG4F1YWtcGwTUM&clientType=android&sign=android&city=" + 合肥
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
