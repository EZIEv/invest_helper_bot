# Importing inbuilt modules 
import logging

# Importing external modules
import psycopg2

# The abstract class for creating a connection with database in Postgre
class Postgre_Connection():
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.connection = None
        try:
            self.connection = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )

            logging.info(f"The connection with {db_name} was established")
        except psycopg2.OperationalError as e:
            logging.critical(f"The error '{e}' occurred")
        except:
            logging.critical(f"Something wrong with {db_name}. Connection wasn't established")
