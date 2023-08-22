# Importing custom modules
from Stock_interaction.alpha_vantage_construct import AlphaVantageConstruct
from Stock_interaction.represent import Represent

# Creating class for interaction with stocks' data
class Stocks(AlphaVantageConstruct, Represent):
    def __init__(self):
        super().__init__(self)

    # Getting and representing overview's data
    def company_overview(self, ticker: str) -> str:
        # Getting data from AlphaVantage
        response = self.get_company_overview_alpha_vantage(ticker)

        if not response:
            return "Данный тикер не найден"

        # Representing data
        return self.company_overview_represent(response)