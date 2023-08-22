# Importing inbuilt modules
import requests
import logging


# Import custom modules
import config


# Class for interaction with stocks' info
class AlphaVantageConstruct():
    def __init__(self, *args):
        self.__alpha_url = f'https://www.alphavantage.co/query?apikey={config.alphavantage_api_key}&'

    # Getting overview of a company
    def get_company_overview_alpha_vantage(self, symbol: str) -> dict:
        self.__overview_alpha_url = self.__alpha_url + f'function=OVERVIEW&symbol={symbol}'

        try:
            response = requests.get(self.__overview_alpha_url).json()
        except:
            logging.error("Can't get data from AlphaVantage")
            return {}

        return response