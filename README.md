Домашний бот для контроля закаченных торрентов и их добавления.

<details>

<summary>Запуск в докер контейнере</summary>

```
git clone git@github.com:catstyle1101/bot_home.git
cd bot_home
touch .env
echo TELEGRAM_TOKEN_MANHATTAN=1373035347:AAFKzpaiFHBTBLK0W1BwQAEVevOHw3u24ds >> .env
docker compose up -d --build
```

</details>

<details>
<summary>Деплой бота как демона в системе:</summary>

```
sudo tee /etc/systemd/system/bot.service << END
[Unit]
Description=Telegram bot
After=network.target

[Service]
Type=simple
User=ubuntu
Restart=always
WorkingDirectory=/home/ubuntu/code/bot_home/
Restart=on-failure
RestartSec=5
ExecStart=/bin/sh -c 'cd /home/ubuntu/code/bot_home/ && . ./env/bin/activate && pip install -r requirements.txt && python bot.py'

[Install]
WantedBy=multi-user.target
END

sudo systemctl daemon-reload
sudo systemctl enable bot.service
sudo systemctl start bot.service
```
</details>
