'''----------------DESCRIPTION---------------

    This module starts the bot and here are 
    implemented all frontend functions.

    Realized commands:
    *commands that don't display in menu and
    available only for admins

        - start (adds user to database and
                 sends welcome message)

        - help (sends a message about 
                bot's functionality)

        - support (allows a user to 
                   contact with admin and 
                   allows an admin to 
                   answer on users' 
                   messages)

        - *answer (allows an admin to answer
                   on users' messages)

        - stop (removes a user from 
                database and sends a 
                farewell message)

        - overview (gets from user a ticker
                    of a company and sends 
                    all financial perfomance
                    of the company)

        - profile (allows a user to adjust
                   news' subscriptions and
                   notifications)

    -----------------------------------------'''


# Importing inbuilt modules
import logging


# Importing external modules
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext, filters


# Importing custom modules
import config
from User_interaction.user import User
from Stock_interaction.stocks import Stocks
from User_interaction.user_states import UserState


'''---------------INITIALIZATING---------------'''


# Initializating logger file
logging.basicConfig(level=logging.INFO, filename=config.log_file, filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")


# Initializating custom classes
bot = Bot(config.bot_api_key, parse_mode='HTML')     # Initializating of connection with TelegramAPI
dp = Dispatcher(bot, storage=MemoryStorage())    # Initializating of dispatcher 
user = User("users", "postgres", config.users_db_password, config.users_db_ip, config.users_db_port)    # Initializating connection with 'users' database
stock = Stocks()    # Initializating class of Stocks with methods for stocks' analyzation 

news_agregators_grouped = config.news_agregators_grouped    # Initializating dict {news country: (news agregators)}
news_agregators = [news_agregator[0] for news_agregator in config.news_agregators] # Initializating list of news agregators


# Initializating bot's commands in menu button
async def setup_bot_commands(*args):
    bot_commands = [
        types.BotCommand(command="/profile", description="Управление профилем"),
        types.BotCommand(command="/overview", description="Получить информацию о компании"),        
        types.BotCommand(command="/help", description="Полное руководство по использованию"),
        types.BotCommand(command="/support", description="Связь с разработчиками"),
        types.BotCommand(command="/stop", description="Прекратить использование бота")
    ]

    await bot.set_my_commands(bot_commands)


'''---------------START COMMAND AND WELCOME MESSAGE----------'''


# Start command with user's registration in 'users' database
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("""Я рад, что вы решили воспользоваться моей помощью!\n
Во вкладке "Menu" уже реализован набор комманд для взаимодействия со мной\n
Для более полного ознакомления воспользуйтесь командой /help\n
Чтобы связаться с моими создателями используйте команду /support""")
    
    user.add(message.from_user.id)  # Adding user to 'users' database if doesn't exist


'''---------------HELP COMMAND AND INSTRUCTION MESSAGE---------------'''


# Help command
@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer("""Вот информация о командах по взаимодействию со мной:\n
/support - позволит связаться с моими создателями, передать им свои пожелания или задать вопрос
/overview - позволит получить всю информацию о компании, такие характеристики как капитализация, доходы, EBITDA, PE, дивиденды и многие другие
""")


'''---------------SUPPORT COMMAND---------------'''

# User's part

# Changing user's state to 'support'
@dp.message_handler(commands=['support'])
async def getting_support_message(message: types.Message):
    await message.answer("Введите сообщение для моих создателей:")
    await UserState.support.set()   # Changing user's state to 'support' for getting a message to admin


# Getting user's message, sending it to admin and restoring user's state
@dp.message_handler(state=UserState.support)
async def support(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=754668096, text=f"ID чата: {message.chat.id}\n\nТекст сообщения: {message.text}")
    await message.answer("Ваше сообщение было доставлено моим создателям, вскоре они вам ответят")

    await state.finish()    # Restoring user's state to base


# Admin's part

# Changing admin's state to 'answer_id'
@dp.message_handler(filters.IDFilter(chat_id=754668096), commands=['answer'])
async def getting_id_answer_support(message: types.Message):
    await message.answer("Введите ID чата на сообщение которого вы хотите ответить:")
    await UserState.answer_id.set()     # Changing admin's state to 'answer_id' for getting chat's ID


# Getting chat's ID and changing admin's state to 'answer_message'
@dp.message_handler(filters.IDFilter(chat_id=754668096), state=UserState.answer_id)
async def getting_message_answer_support(message: types.Message, state: FSMContext):
    await state.update_data(chat_id=message.text)   # Writing to dict the chat's ID

    await message.answer("Отлично! Введите сообщение с ответом на запрос:")
    await UserState.answer_message.set()    # Changing admin's state to 'answer message' for getting answer message


# Getting answer message, formating answer, sending it to user and restoring admin's state
@dp.message_handler(filters.IDFilter(chat_id=754668096), state=UserState.answer_message)
async def answer(message: types.Message, state: FSMContext):
    await state.update_data(answer=message.text)    # Writing to dict the answer message
    data = await state.get_data()

    try:
        await bot.send_message(chat_id=data['chat_id'], text=f"Ответ на ваше сообщение от создателей:\n\n{data['answer']}")
    except:
        await message.answer("Неправильный ID чата, проверьте его ввод и попробуйте снова")
    else:
        await message.answer("Ваш ответ был отправлен")

    await state.finish()    # Restoring admin's state to base


'''---------------STOP COMMAND AND FAREWELL MESSAGE---------------'''


# Stop command with user's deleting
@dp.message_handler(commands=['stop'])
async def send_goodbye(message: types.Message):
    await message.answer("""Мне очень жаль, что вы уходите.\n
Если у вас есть какие-либо пожелания по улучшению моей работы, вы можете связаться с моими создателями при помощи команды /support.

Чтобы снова начать со мной работать, воспользуйтесь командой /start""")

    user.remove(message.from_user.id)   # Deleting user from users database if exists


'''---------------OVERVIEW COMMAND---------------'''


# Changing user's state to 'company_overview'
@dp.message_handler(commands=['overview'])
async def get_ticker_for_overview(message: types.Message):
    await message.answer("Введите тикер компании: ")
    await UserState.company_overview.set()  # Changing user's state to 'company_overview' for getting company's ticker


# Getting ticker of a company, sending overview and restoring user's state 
@dp.message_handler(state=UserState.company_overview)
async def overview(message: types.Message, state: FSMContext):
    response = stock.company_overview(message.text.upper())     # Getting overview of the company
    await message.answer(response)

    await state.finish()    # Restoring user's state to base


'''---------------PROFILE COMMAND---------------'''


'''---------------MAIN PAGE---------------'''


# Profile command showes inline keyboard for adjusting user's profile
@dp.message_handler(commands=['profile'])
@dp.callback_query_handler(lambda callback: callback.data == 'profile_main_page')
async def profile(message: types.Message):

    # Initializating inline keyboard
    reply_markup = types.inline_keyboard.InlineKeyboardMarkup()

    reply_markup.row(*[
        types.inline_keyboard.InlineKeyboardButton('Новости', callback_data='profile_news_page')
    ])

    if not hasattr(message, 'message'):     # If function called within command
        await message.answer("Выберите действие: ", reply_markup=reply_markup)
    else:   # If function called within callback
        await bot.edit_message_text("Выберите действие: ", chat_id=message.message.chat.id, message_id=message.message.message_id, reply_markup=reply_markup)


'''--------------NEWS PAGE---------------'''


# Showes inline keyboard with countries
@dp.callback_query_handler(lambda callback: callback.data == 'profile_news_page')
async def news_countries_page(callback: types.CallbackQuery):

    # Initializating inline keyboard
    reply_markup = types.inline_keyboard.InlineKeyboardMarkup()

    for news_country in news_agregators_grouped:
        reply_markup.row(*[
            types.inline_keyboard.InlineKeyboardButton(news_country, callback_data=news_country)
        ])
    
    reply_markup.row(*[
        types.inline_keyboard.InlineKeyboardButton('Назад', callback_data='profile_main_page')
    ])

    await bot.edit_message_text("Выберите страну: ", chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=reply_markup)


# Showes inline keyboard with news agregators for chosen country
@dp.callback_query_handler(lambda callback: callback.data in news_agregators_grouped)
async def news_agregators_page(callback: types.CallbackQuery):

    # Initializating inline keyboard
    reply_markup = types.inline_keyboard.InlineKeyboardMarkup()

    for news_agregator in news_agregators_grouped[callback.data]:
        reply_markup.row(*[
            types.inline_keyboard.InlineKeyboardButton(news_agregator, callback_data=f'{news_agregator}|{callback.data}')
        ])

    reply_markup.row(*[
        types.inline_keyboard.InlineKeyboardButton('Назад', callback_data='profile_news_page')
    ])

    await bot.edit_message_text(f"Выберите агрегатор новостей: ", 
                                chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=reply_markup)


# Showes inline keyboard for adjusting settings of chosen news agregator
@dp.callback_query_handler(lambda callback: callback.data.split('|')[0] in news_agregators)
async def news_agregator_page(callback: types.CallbackQuery):

    # Split callback on news_resource_name and news_group
    news_agregator, news_country = callback.data.split('|')

    # Initializating inline keyboard
    reply_markup = types.inline_keyboard.InlineKeyboardMarkup()

    # Adaptes text to user's status for news
    adapt_text_to_status = lambda text, status: '✅' + text + '✅' if status else '❌' + text + '❌'

    # Text for inline buttons
    subscribe = adapt_text_to_status('Подписка', user.news_status_check(callback.from_user.id, 
                                                                        news_agregator.lower().replace(' ', '_'), 
                                                                        'users_news'))
    silent_mode = adapt_text_to_status('Тихий режим', user.news_status_check(callback.from_user.id, 
                                                                          news_agregator.lower().replace(' ', '_'), 
                                                                          'users_news_notification'))

    reply_markup.row(*[
        types.inline_keyboard.InlineKeyboardButton(subscribe, callback_data=f'{subscribe}|{news_country}'),
        types.inline_keyboard.InlineKeyboardButton(silent_mode, callback_data=f'{silent_mode}|{news_country}')
    ])

    reply_markup.row(*[
        types.inline_keyboard.InlineKeyboardButton('Назад', callback_data=news_country)
    ])

    await bot.edit_message_text(f"Настройки <b>{news_agregator}</b>: ", chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=reply_markup)


# Changes user's news settings in database
@dp.callback_query_handler(lambda callback: 'Подписка' in callback.data or 'Тихий режим' in callback.data)
async def news_status_change(callback: types.CallbackQuery):

    # Choosing table in db for changing status
    if 'Подписка' in callback.data:
        table = 'users_news'
    elif 'Тихий режим' in callback.data:
        table = 'users_news_notification'

    # Determine status for changing that different from current
    status = True if callback.data[0] == '❌' else False

    news_agregator = callback.message.text[10:len(callback.message.text) - 1]
    news_country = callback.data.split('|')[1]

    # Changing status of user
    if not user.news_status_change(callback.from_user.id, 
                                   news_agregator.lower().replace(' ', '_'),
                                   status, table):
        await bot.send_message(callback.from_user.id, "Извините, но на данный момент я не могу установить связь с базой данных, мои создатели уже решают данную проблему...")

    callback.data = f'{news_agregator}|{news_country}'

    await news_agregator_page(callback)




# Starting the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands)