# Importing external modules
from aiogram.dispatcher.filters.state import StatesGroup, State

# Creating class of user's states
class UserState(StatesGroup):
    # States for admins
    answer_id = State()
    answer_message = State()

    # States for users
    company_overview = State()
    support = State()