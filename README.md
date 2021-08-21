## Volume Remote Control Bot for MacOS

Simple Bot to RC your mac volume via Telegram.

### Installation

- Fetch the token from the TG Bot Father and put it into `./token` file.
- Prepare the environment:
```
$> python3 -m venv venv
$> ./venv/bin/pip3 install -r requirements.txt

```
- Then just run the bot on your mac. You'll need to use you TG nickname
```
$> ./venv/bin/python3 main.py --user <nickname>
```
- I personally prefer to use pm2:
```
$> npm install -g pm2
$> pm2 start -n rc ./venv/bin/python3 -- main.py --user <nickname>
```

### CLI Arguments

- user - (required) your nickname in TG. I need it to control permission.
- token - path to the token.
- step - how fast the volume should be changed


### Control

Just use the buttons to control the bot. Have fun!
