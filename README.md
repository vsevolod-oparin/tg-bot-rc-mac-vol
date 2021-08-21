## Volume Remote Control Bot for MacOS

Simple Bot to RC your mac volume via Telegram.

### Installation

- Fetch the token from the TG Bot Father and put it into `./token` file.
- Prepare the environment:
```
$> python3 -m venv venv
$> ./venv/bin/pip3 install -r requirements.txt

```
- Then just run the bot on your mac.
```
$> ./venv/bin/python3 -- main.py
```
- I personally prefer to use pm2:
```
$> npm install -g pm2
$> pm2 start -n rc ./venv/bin/python3 -- main.py
```

### Control

Just use the buttons to control the bot. Have fun!