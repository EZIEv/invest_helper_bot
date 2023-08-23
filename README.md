# Invest Helper Bot v2.02:alpha

## Makes financial decisions easier

### (|_o_o_|) [Link to the bot](https://t.me/invst_helper_bot) (|_o_o_|)

---

### ❓ Why should you use this bot?  

The main audience for this bot is private investors who trade stocks. This bot can assist them in making decisions about various companies based on their financial performance. Investors can receive the latest economic news from different news aggregators worldwide. All notifications are received through Telegram, eliminating the need for subscriptions to multiple resources or extra apps. All functionality is consolidated within a single messenger.

These are just some of the planned functions that have already been implemented. For additional functionality, please refer to the "Future plans" section.

---
### ✨ Realized features

+ **Support Command:** This feature enables users to contact admins via the bot for assistance.
+ **Overview Command:** Users can request financial performance details about a company by providing its ticker symbol.
+ **News:** Users can adjust their subscriptions to various economic news aggregators in their personal profiles, and they will receive the latest news from them.

---
### 🚀 Getting started

To start using this bot, you need to perform a quick setup.

Firstly, obtain your own free API key from _**[alphavantage](https://www.alphavantage.co/support/#api-key)**_.
Next, create a bot on _**[telegram](https://t.me/BotFather)**_ and save its API key. I use two bots: one for primary use and another for testing, although you can use just one.
With these keys in hand, you're ready to proceed with the bot's configuration.

Navigate to the folder containing this repository and locate the **'.env'** file.

```
ALPHAVANTAGE_API_KEY = "pass here your alphavantage api key"
BOT_API_KEY = "pass here your telegram bot api key"
TEST_BOT_API_KEY = "pass here your second telegram bot api key or leave an empty string if you don't have it"
USERS_DB_PASSWORD = "create a password for access to database"
```

Now, open the **'docker-compose.yaml'** file located in the same folder.

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

We're now prepared to build the Docker image.

```sh
docker build --tag username/invest_bot:v2.02_alpha .
```

Next, initiate the bot.

```sh
docker-compose up -d
```

---
### 📋 Problems

Here are some issues that will be addressed in the future:
1. **Container Separation:**  **'news.py'** and **'bot.py'** are currently operating within a single container. It would be beneficial to separate them and allow them to function independently. This separation is crucial because if one of them fails, the entire container is forced to restart.
2. **Using an ORM:** Interaction with the database is currently based on native SQL queries. Utilizing an Object-Relational Mapping (ORM) system would be preferable, as it enhances the speed of code development and improves readability. (In this project, I have used SQL queries solely for practice purposes.)
3. **Categorizing RSS Channels:** The **'RSS_pars.py'** script currently only parses entire RSS channels based on provided links. To accommodate a larger number of usable news aggregators and improve user experience, it is necessary to implement a function that categorizes channels.
4. **Parsing Non-RSS Sources:** Given the information from the third point, **'RSS_pars.py'** is unable to parse news aggregators lacking an RSS channel. Consequently, a new class needs to be developed to handle parsing for non-RSS news aggregators.
   
This project represents my initial venture as a programmer and my first practical experience. While I recognize there may be additional issues, I would greatly appreciate any insights you could provide.

---
### 🖥️ Future plans

+ Users will be able to create a personal portfolio and monitor stock quotes.
+ Users can set quote targets and receive notifications upon achieving them.
+ Users will have access to the latest press releases and reports from companies.
+ Users can track the dividends calendar.
+ Users can customize news based on companies in their personal profiles.
+ Develop a website with an admin panel, giving administrators control over the bot and databases.
+ Establish an educational website providing training on financial investments.

Feel free to offer additional suggestions or features, and I will certainly consider them. If you have any more text to review or need further assistance, don't hesitate to ask!

---
### 👨‍💻 Authors

_**Samuilov Danil**_ - eziev (_https://github.com/EZIEv_)

---
