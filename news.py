'''----------------DESCRIPTION---------------

    This module starts parsing data from 
    aggregator URLs in the config file and 
    sends it to users from the database who 
    are subscribed to this aggregator.

    -----------------------------------------'''

# Importing inbuilt modules
import time
import asyncio
import logging


# Importing external modules
from aiogram import Bot, utils


# Importing custom modules
import config
from User_interaction.user import User
from News_interaction.RSS_pars import RSS_pars


'''---------------INITIALIZATING---------------'''


# Initializating logger file
logging.basicConfig(level=logging.INFO, filename=config.log_file, filemode='a', \
                    format="%(asctime)s %(levelname)s %(message)s")


# Initializating custom modules
bot = Bot(config.bot_api_key, parse_mode='HTML') # Initializating of connection with TelegramAPI
user = User("users", "postgres", config.users_db_password, config.users_db_ip, config.users_db_port) # Initializating connection with 'users' database
rss_pars = RSS_pars() # Initializating class for interaction with RSS news channels


'''---------------MAIN FUNCTION---------------'''


# Function for retrieving news, analyzing it, and sending it to the user
async def send_news_to_user(news_agregator: str, news_agregator_url: str):
    while True:
        async for news in rss_pars.news_pars(news_agregator_url):    # Getting news from RSS channel
            if not await rss_pars.is_news_in_old_news(news[2], news_agregator):    # Checking for the existence of news in the old news
                async for user_with_news_agregator in user.get_users_with_news(news_agregator):      # Getting all users who are subscribed to this news resource
                    # Sending a message to a user
                    try:
                        # With photo if image exists
                        if news[0]:
                            await bot.send_photo(user_with_news_agregator, news[0], 
                                                caption=f'<b><i>{news[1]}</i></b>\n\n<a href="{news[2]}">Ссылка на ресурс</a>\n\n{news[3]}', 
                                                disable_notification=user.news_status_check(user_with_news_agregator, news_agregator, 'users_news_notification'))           
                        # Only a text message if there is no image
                        else:
                            await bot.send_message(user_with_news_agregator, f'<b><i>{news[1]}</i></b>\n\n<a href="{news[2]}">Ссылка на ресурс</a>\n\n{news[3]}', 
                                            disable_web_page_preview=True, 
                                            disable_notification=user.news_status_check(user_with_news_agregator, news_agregator, 'users_news_notification'))
                            
                    # If a user has blocked the bot or has been deactivated
                    except utils.exceptions.Unauthorized:
                        user.remove(user_with_news_agregator)

                    # If the message is too long, send the message without the description
                    except utils.exceptions.BadRequest:
                        if news[0]:
                            await bot.send_photo(user_with_news_agregator, news[0], 
                                                caption=f'<b><i>{news[1]}</i></b>\n\n<a href="{news[2]}">Ссылка на ресурс</a>', 
                                                disable_notification=user.news_status_check(user_with_news_agregator, news_agregator, 'users_news_notification'))
                        else:
                            await bot.send_message(user_with_news_agregator, f'<b><i>{news[1]}</i></b>\n\n<a href="{news[2]}">Ссылка на ресурс</a>', 
                                            disable_web_page_preview=True, 
                                            disable_notification=user.news_status_check(user_with_news_agregator, news_agregator, 'users_news_notification'))    
                            

        await rss_pars.recreate_old_news_backup_file(news_agregator)    # Creating backup file with old news

        await asyncio.sleep(60)     # Timeout for descend loading on RSS server


'''---------------START FUNCTION---------------'''


# Creating tasks for asyncronous parsing news
async def main():
    tasks = []
    for news_agregator in rss_pars.news_agregators:
        tasks.append(asyncio.create_task(send_news_to_user(*news_agregator)))

    await asyncio.gather(*tasks)




# Starting the program
if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            logging.critical(f"Something wrong with news service\n\n{e}")

            time.sleep(60)
