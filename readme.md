<p style="text-align: center; font-size: 40px; color: #FFD700; font-family: sans-serif;">Invest Helper Bot v2.02:alpha</p>

<p style="text-align: center; font-size: 18px; color: #C0C0C0; font-family: sans-serif;">Makes financial decisions easier</p>

---

<p style="text-align: center; font-size: 18px; font-family: sans-serif;">(|_o_o_|) <a href="https://t.me/invst_helper_bot" style="color: #C0C0C0; text-decoration: underline">Link to the bot</a> (|_o_o_|)</p>

---
<br>
<p style="font-family: sans-serif; font-size: 18px;">❓ Why you should use this bot?</p>  

<p style="fint-family: sans-serif; font-size: 16px; margin-left: 16px;">The main auditory is the private investors that use stocks. This bot can help them make decisions about different companies based on financial perfomance, investors can adjust getting last economic's news from different news agregators all over the world. All notifications they recieve in telegram, no subscriptions on many resources, no extra apps. All functionality only in one messenger.<br><br>It is just a part of the planned functions that have been already realized. For more functionality check "Further plans".</p>

---
<br>
<p style="font-family: sans-serif; font-size: 18px;">✨ Realized features</p> 

<p style="font-family: sans-serif; font-size: 16px; margin-left: 16px;"><ul><li style="font-family: sans-serif; font-size: 16px;">Support command (allows a user to contact with admins via bot)<li style="font-family: sans-serif; font-size: 16px;">Overview command (sends financial perfomance about the company by a ticker)<li style="font-family: sans-serif; font-size: 16px;">News (user adjusts subscribes on the different economic's news agregators in the personal profile and recieves last news from them)</ul></p>

---
<br>
<p style="font-family: sans-serif; font-size: 18px;">🚀 Getting Started</p>

<p style="font-family: sans-serif; font-size: 16px; margin-left: 16px;">For starting this bot you need to do a small setup.<br><br>First of all get your own free api key from the <a href="https://www.alphavantage.co/support/#api-key">alphavantage</a>.<br>Then you need to create a bot in <a href="https://t.me/BotFather">telegram</a> and save its api key. I use two bots: the first is main and the second is for tests, but you can use only one.<br>Now you have all the keys you need and we can go to configuration of the bot.<br><br>Open a folder with this repository and choose a file .env</p>

```
ALPHAVANTAGE_API_KEY = "pass here your alphavantage api key"
BOT_API_KEY = "pass here your telegram bot api key"
TEST_BOT_API_KEY = "pass here your second telegram bot api key or leave an empty string if you don't have it"
USERS_DB_PASSWORD = "create a password for access to database"
```

<p style="font-family: sans-serif; font-size: 16px; margin-left: 16px;">Now open docker-compose.yaml in the same folder</p>

```yaml
version: '3.5'

services:
  users_db:
    container_name: users
    image: postgres:bullseye
    restart: always
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=users
      - POSTGRES_PASSWORD={pass here you USERS_DB_PASSWORD from .env}
      - POSTGRES_USER=postgres
    volumes:
      - ./DataBase/data:/var/lib/postgresql/data
      - ./DataBase/init.sql:/docker-entrypoint-initdb.d/init.sql
  invest_bot:
    container_name: invest_bot
    depends_on:
      - users_db
    restart: always
    build: .
    network_mode: host
    volumes:
      - ./temp:/invest_bot/temp
```

<p style="font-family: sans-serif; font-size: 16px; margin-left: 16px;">Now we are ready to build Docker image</p>

```sh
docker build --tag username/invest_bot:v2.02_alpha .
```

<p style="font-family: sans-serif; font-size: 16px; margin-left: 16px;">And start the bot</p>

```sh
docker-compose up -d
```

---
<br>
<p style="font-family: sans-serif; font-size: 18px;">📋 Problems</p>

<p style="font-family: sans-serif; font-size: 16px; margin-left: 16px;">Here are some problems that will be solved in the future: <ol style="font-family: sans-serif; font-size: 16px;"><li>news.py and bot.py are working in one container. It would be better if they were separated and worked independently, because if one of them breaks down, the whole container is rebooted.<li>Interaction with the database occurs through the native SQL-queries. It's better if you use ORM because it increases speed of code's writing and its readability. (I have used the SQL-queries here only like a practice)<li>RSS_pars.py parses only whole rss channel by the link, and for increasing quantity of news agregators suitable for using, it is need to add a function that divides channel on categories.<li>According to the third paragraph RSS_pars.py can't pars news agregators without rss channel. So we need to create a new class that parses non-rss news agregators.</ol></p>
<p style="font-family: sans-serif; font-size: 16px;">This is my first project and the first real practice like a programmer, so there are more problems and it would be great if you noticed them.</p>

---
<br>
<p style="font-family: sans-serif; font-size: 18px;">🖥️ Further plans</p>

<p style="font-family: sans-serif; font-size: 16px; margin-left: 16px;"><ul style="font-family: sans-serif; font-size: 16px; margin-left: 16px;"><li>Users can create personal portfolio and monitor stocks' quotes<li>Users can set quotes targets and recieve notifications on their achievements<li>Users can recieve last press releases and reports of the companies<li>Users can monitor dividends calendar<li>Users can adjust news by the companies in personal profile<li>Create a site with the admin-panel where admins can control the whole bot and the whole databases<li>Create a training site about financial investments</ul></p>

<p style="font-family: sans-serif; font-size: 16px; margin-left: 16px;">You can offer own features and i will certainly consider them.</p>

---
<br>
<p style="font-family: sans-serif; font-size: 18px;">👨‍💻 Authors</p>

<p style="font-family: sans-serif; font-size: 16px; margin-left: 16px;">Samuilov Danil - eziev (https://github.com/EZIEv)</p>

---
<br>