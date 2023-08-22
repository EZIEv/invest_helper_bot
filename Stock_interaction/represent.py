# Importing inbuilt modules
import logging

# Creating class for representing different data
class Represent():
    # Representing data from overview
    def company_overview_represent(self, overview_data: dict) -> str:
        # If there is no data, so there is no data
        for param in overview_data:
            if overview_data[param] == 'None':
                overview_data[param] = "Нет данных"

        # Representing big numeric parameteres
        for param in ('MarketCapitalization', 'RevenueTTM', 'GrossProfitTTM', 'EBITDA'):
            try:
                overview_data[param] = f"{round(int(overview_data[param]) / 10**9, 3)} млрд. {overview_data['Currency']}"
            except ValueError:
                overview_data[param] = "Нет данных"
            except:
                logging.error("Something wrong with representing overview's data")
                return ''

        # Formating the result in str format
        overview_result = f"""<b>{overview_data['Name']} | {overview_data['Symbol']} | {overview_data['Exchange']} | {overview_data['Currency']}</b>\n
Тип бумаги: {overview_data['AssetType']}\n
Сектор: {overview_data['Sector']}\n
Индустрия: {overview_data['Industry']}\n
Описание: {overview_data['Description']}\n
Капитализация: {overview_data['MarketCapitalization']}\n
Доход ТТМ: {overview_data['RevenueTTM']}\n
Валовая прибыль ТТМ: {overview_data['GrossProfitTTM']}\n
EBITDA: {overview_data['EBITDA']}\n
PE: {overview_data['PERatio']}\n
Балансовая стоимость: {overview_data['BookValue']} {overview_data['Currency']}\n
Операционная маржа ТТМ: {overview_data['OperatingMarginTTM']}%\n
Доход на акцию ТТМ: {overview_data['RevenuePerShareTTM']} {overview_data['Currency']}\n
Прибыль на акцию: {overview_data['EPS']} {overview_data['Currency']}\n
Разводненная прибыль на акцию ТТМ: {overview_data['DilutedEPSTTM']}\n
Дивиденды на акцию: {overview_data['DividendPerShare']} {overview_data['Currency']}\n
Дивидендная доходность: {overview_data['DividendYield']}%\n
Рентабельность собственного капитала ТТМ: {overview_data['ReturnOnEquityTTM']}%\n
Рентабельность активов ТТМ: {overview_data['ReturnOnAssetsTTM']}%\n
Рентабельность продаж: {overview_data['ProfitMargin']}%\n
Прогнозируемая цена аналитиков: {overview_data['AnalystTargetPrice']} {overview_data['Currency']}\n
Прогнозируемый показатель цена / прибыль на акцию: {overview_data['ForwardPE']}\n
Цена / выручка ТТМ: {overview_data['PriceToSalesRatioTTM']}\n
Цена / балансовая стоимость: {overview_data['PriceToBookRatio']}\n
EV / доход: {overview_data['EVToRevenue']}\n
EV / EBITDA: {overview_data['EVToEBITDA']}\n
Бета: {overview_data['Beta']}\n
52-недельный максимум: {overview_data['52WeekHigh']} {overview_data['Currency']}\n
52-недельный минимум: {overview_data['52WeekLow']} {overview_data['Currency']}\n
50-дневная скользящая средняя: {overview_data['50DayMovingAverage']} {overview_data['Currency']}\n
200-дневная скользящая средняя: {overview_data['200DayMovingAverage']} {overview_data['Currency']}\n
Акций в обращении: {overview_data['SharesOutstanding']}\n
Дата выплаты дивидендов: {overview_data['DividendDate']}\n
Прошлая дата выплаты дивидендов: {overview_data['ExDividendDate']}\n
"""

        return overview_result