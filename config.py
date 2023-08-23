# Importing inbuilt modules
import os


# Importing external modules
from dotenv import find_dotenv, load_dotenv


# Finding and uploading environment variables from .env
load_dotenv(find_dotenv())




# API keys
test_bot_api_key = os.environ.get("TEST_BOT_API_KEY")

bot_api_key = os.environ.get("BOT_API_KEY")

alphavantage_api_key = os.environ.get("ALPHAVANTAGE_API_KEY")




# Users database
users_db_ip = "127.0.0.1"

users_db_port = "5432"

users_db_password = os.environ.get("USERS_DB_PASSWORD")




# Log file
log_file = "invest_bot.log"




# To add a new news agregator, add a new tuple in news_agregator ('Name of news agregator', 'link to RSS of news agregator') and 
# add it to news_agregators_grouped dict to respective group or create another one
news_agregators_grouped = {'Америка': ('CNBC',
                                      'Wall Street Journal',
                                      'Marketwatch',
                                      'Bloomberg',
                                      'Forbes'),
                          'Россия': ('Коммерсантъ',
                                     'Лента',
                                     'Russia Today'),
                          'Казахстан': ('KASE News',)}

news_agregators = (('CNBC', 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258'),
                  ('Wall Street Journal', 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml'),
                  ('Marketwatch', 'http://feeds.marketwatch.com/marketwatch/marketpulse/'),
                  ('Bloomberg', 'http://feeds.marketwatch.com/marketwatch/marketpulse/'),
                  ('Forbes', 'https://www.forbes.com/investing/feed2'),
                  ('Коммерсантъ', 'https://www.kommersant.ru/RSS/section-economics.xml'),
                  ('Лента', 'https://lenta.ru/rss/news/economics'),
                  ('Russia Today', 'https://www.rt.com/rss/business/'),
                  ('KASE News', 'https://kase.kz/ru/news/rss/'))
