# Invest Helper Bot v2.02:alpha

## Makes financial decisions easier

### (|_o_o_|) <a href="https://t.me/invst_helper_bot">Link to the bot</a> (|_o_o_|)

---

### ❓ Why you should use this bot?  

The main auditory is the private investors that use stocks. This bot can help them make decisions about different companies based on financial perfomance, investors can adjust getting last economic's news from different news agregators all over the world. All notifications they recieve in telegram, no subscriptions on many resources, no extra apps. All functionality only in one messenger.

It is just a part of the planned functions that have been already realized. For more functionality check "Further plans".

---
### ✨ Realized features

+ Support command (allows a user to contact with admins via bot)
+ Overview command (sends financial perfomance about the company by a ticker)
+ News (user adjusts subscribes on the different economic's news agregators in the personal profile and recieves last news from them)

---
### 🚀 Getting Started

For starting this bot you need to do a small setup.<br><br>First of all get your own free api key from the _**[alphavantage](https://www.alphavantage.co/support/#api-key)**_.
Then you need to create a bot in _**[telegram](https://t.me/BotFather)**_ and save its api key. I use two bots: the first is main and the second is for tests, but you can use only one.
Now you have all the keys you need and we can go to configuration of the bot.

Open a folder with this repository and choose a file .env

```
ALPHAVANTAGE_API_KEY = "pass here your alphavantage api key"
BOT_API_KEY = "pass here your telegram bot api key"
TEST_BOT_API_KEY = "pass here your second telegram bot api key or leave an empty string if you don't have it"
USERS_DB_PASSWORD = "create a password for access to database"
```

Now open docker-compose.yaml in the same folder

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

Now we are ready to build Docker image

```sh
docker build --tag username/invest_bot:v2.02_alpha .
```

And start the bot

```sh
docker-compose up -d
```

---
### 📋 Problems

Here are some problems that will be solved in the future: 
1. news.py and bot.py are working in one container. It would be better if they were separated and worked independently, because if one of them breaks down, the whole container is rebooted.
2. Interaction with the database occurs through the native SQL-queries. It's better if you use ORM because it increases speed of code's writing and its readability. (I have used the SQL-queries here only like a practice)
3. RSS_pars.py parses only whole rss channel by the link, and for increasing quantity of news agregators suitable for using, it is need to add a function that divides channel on categories.
4. According to the third paragraph RSS_pars.py can't pars news agregators without rss channel. So we need to create a new class that parses non-rss news agregators.
   
This is my first project and the first real practice like a programmer, so there are more problems and it would be great if you noticed them.

---
### 🖥️ Further plans

+ Users can create personal portfolio and monitor stocks' quotes
+ Users can set quotes targets and recieve notifications on their achievements
+ Users can recieve last press releases and reports of the companies
+ Users can monitor dividends calendar
+ Users can adjust news by the companies in personal profile
+ Create a site with the admin-panel where admins can control the whole bot and the whole databases
+ Create a training site about financial investments

You can offer own features and i will certainly consider them.

---
### 👨‍💻 Authors

_**Samuilov Danil**_ - eziev (_https://github.com/EZIEv_)

---
