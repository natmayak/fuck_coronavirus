# fuck_coronavirus
Fuck_coronavirus is a telegram bot that helps you not to screw up your hygiene in these turbulent covid times. 
The bot is essentially ironic and sometimes strict to make sure you do what it tells you.
 
### Reminders 
You'll get basic reminders every 20 minutes to wash your hands and do other important things for your health.
### Pharmacies
The bot also helps you find the nearest pharmacies around you. 
Share your location with the bot and it will send you the names of the 3 closest pharmacies linked to Yandex.Maps.

<img src= "https://user-images.githubusercontent.com/61066838/83327190-c0a97280-a282-11ea-9db4-d0ba6d9160f7.jpg" width = "260" height = "466" >

We are using [MongoDB](https://www.mongodb.com) and [Yandex Organizations](https://tech.yandex.ru/maps/geosearch/doc/concepts/request-docpage/).

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/natmayak/fuck_coronavirus/graphs/commit-activity)

## Getting started

From console run:
```
git clone https://github.com/natmayak/fuck_coronavirus.git
pip install -r requirments.txt
```
## Tuning up

Go to settings.txt, insert your own proxy, API keys and add more [emojis](http://www.fileformat.info/info/emoji/list.htm) if you like: 

```
PROXY = {'proxy_url': 'socks5://insert_your_proxy:1080',
         'urllib3_proxy_kwargs': {'username': 'insert_your_username'', 'password': 'insert_your_password'}}

API_KEY = '<TelegramBot API key from BotFather>'

USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':heart:', ':fire:', ':rocket:', ':earth_americas:']

API_KEY_YNDX='<Yandex API key>'

MONGO_LINK = '<Link to MongoDB>'

MONGO_DB = 'Users'
```

## Use cases

The bot is made in connection with covid-2019 restrictions.

However you can use this bot as a template for other purposes if you require the following basic functions:

* send any other regular reminders (you can change the description of actions and buttons)
* send a number of supermarkets, shops and other organisations based on user location (you can change the type of organisations taken from Yandex) 
* customise ReplyKeboardMarkup and InlineKeyboardMarkup buttons to your needs.

## License 
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)

This project is [MIT Licensed](https://github.com/natmayak/fuck_coronavirus/blob/master/LICENSE)

© 2020 [Yury Prokhorov](https://github.com/5071177) and [Nat Nikulina](https://github.com/natmayak)
