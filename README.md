# Telegram Bot for check devman tasks



Below parameters declared as environment variables, don't forget to set up:
```
export TELEGRAM_TOKEN='telegram token'
export DVMN_AUTHORIZATION_TOKEN='Devman Authorization token'
export TELEGRAM_USER_CHAT_ID='telegram_user_chat id'
export NOTIFICATION_TELEGRAM_TOKEN = 'second telegram token'

```


## How to Use

Step 1. Register new telegram bot for development purposes, get the new token. [@BotFather](https://telegram.me/botfather)

Step 2. Install modules from requirements

Step 3. Launch bot


Example of creating a new virtual environments and launch on Linux , Python 3.5:

```
virtualenv "name_of_virtualenv"
source "name_of_virtualenv"/bin/activate
pip install -r requirements.txt
python3 dvmn_bot.py

```


### How to deploy on Heroku(before need to install heroku cli)


```
heroku login -i
heroku create
git push heroku master
heroku config:set TELEGRAM_TOKEN='telegram token'
heroku config:set DVMN_AUTHORIZATION_TOKEN='Devman Authorization token'
heroku config:set TELEGRAM_USER_CHAT_ID='telegram_user_chat id'
heroku config:set NOTIFICATION_TELEGRAM_TOKEN = 'second telegram token'
sheroku ps:scale bot=1
```

