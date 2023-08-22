# Importing inbuilt modules
import logging


# Importing custom modules
from DataBase.postgre_connection import Postgre_Connection


# Class for interaction with user's data
class User(Postgre_Connection):
    # Initializating connection with database and initializating config parameters
    def __init__(self, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str):
        super().__init__(db_name, db_user, db_password, db_host, db_port)
        self.__db_name = db_name
        self.__cur = self.connection.cursor()


    '''---------------ADD FUNCTION---------------'''


    # Adding user's info in database
    def add(self, user_id: int) -> bool:
        try:
            self.__cur.execute("INSERT INTO users_data (user_id) SELECT %s \
                               WHERE NOT EXISTS (SELECT user_id FROM users_data WHERE user_id = %s)", (user_id, user_id))
            self.__cur.execute("INSERT INTO users_news (user_id) SELECT %s \
                               WHERE NOT EXISTS (SELECT user_id FROM users_news WHERE user_id = %s)", (user_id, user_id))
            self.__cur.execute("INSERT INTO users_news_notification (user_id) SELECT %s \
                               WHERE NOT EXISTS (SELECT user_id FROM users_news_notification WHERE user_id = %s)", (user_id, user_id))
            self.connection.commit()
        except:
            logging.critical(f"Can't add user to {self.__db_name}")
            return False
        else:
            logging.info(f"User {user_id} was added to '{self.__db_name}' database")
            return True


    '''---------------REMOVE FUNCTION---------------'''


    # Removing all user's info from database
    def remove(self, user_id: int):
        try:
            self.__cur.execute("DELETE FROM users_data WHERE user_id = %s", (user_id,))
            self.connection.commit()
        except:
            logging.critical(f"Can't remove user from {self.__db_name}")
            return False
        else:
            logging.info(f"User {user_id} was removed from '{self.__db_name}' database")
            return True


    '''---------------CHECKING USER'S NEWS AGREGATOR's STATUSES---------------'''


    # Checking user's news agregator's statuses
    def news_status_check(self, user_id: int, news_agregator: str, table: str) -> bool:
        try:
            self.__cur.execute(f"SELECT {news_agregator} FROM {table} WHERE user_id = {user_id}")
            self.connection.commit()
        except:
            logging.critical(f"Can't check user's news' statuses")
        else:
            # Checking user on existing in all tables
            try:
                status = self.__cur.fetchone()[0]
            except TypeError:
                self.add(user_id)
                self.news_status_check(user_id, news_agregator, table)
            else:
                return status


    '''---------------CHANGING USERS NEWS STATUSES----------'''


    # Changing user's news status
    def news_status_change(self, user_id: int, news: str, status: bool, table: str) -> bool:
        try:
            self.__cur.execute(f"UPDATE {table} SET {news} = {status} WHERE user_id = {user_id}")
            self.connection.commit()
        except:
            logging.critical(f"Can't change user's news status")
            return False
        else:
            logging.info(f"{user_id} has changed {news} on {status}")
            return True


    '''---------------GETTING ALL USERS WHO HAVE SUBSCRIBE ON NEWS RESOURCE---------------'''


    # Getting all users that have subscribe on news
    async def get_users_with_news(self, news: str) -> tuple:
        try:
            self.__cur.execute(f"SELECT user_id FROM users_news WHERE {news} = true")
            self.connection.commit()
        except:
            logging.critical(f"Can't get users with news for {news}")
        else:
            try:
                for user_with_news in self.__cur.fetchall():
                    yield user_with_news[0]
            # If fetchall is empty, so we catch an Indexerror exception
            except IndexError:
                pass