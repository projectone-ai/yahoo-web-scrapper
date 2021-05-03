from datetime import datetime
import time  # time for converting our data to timestamp format.
import requests  # requests for performing HTTP GET requests.
from bs4 import BeautifulSoup  # BeautifulSoup to organize and parse the HTML content.
from utils import exception_handler  # A custom exception handler to help log the errors.
from models import Stock, Stocks  # Models to structure our stock info.


class YahooFinancialWebScraping:
    website_url = 'https://finance.yahoo.com'
    financial_link_variables = '/quote/{}/history?period1={}&period2={}&interval=1d&filter=history&frequency=1d' \
                               '&includeAdjustedClose=true'

    def __init__(self, symbol: str):
        self.stocks = None
        self.symbol = symbol

    @staticmethod
    @exception_handler
    def convert_date_to_timestamp(date: str) -> str:
        """
        This method has the objective to transform a specific date string variable into timestamp.

        :param date: A string date in the following format (mm/dd/YYYY)
        :return: Return a timestamp of a date in string.
        """
        return str(int(time.mktime(datetime.strptime(date, "%m/%d/%Y").timetuple())))

    @exception_handler
    def extract_financial_data(self, period_1: str, period_2: str) -> list:
        """
        :param period_1: A timestamp date in string to filter from a period.
        :param period_2: A timestamp date in string to filter to a period.

        :return: It should return a structured list of historical prices of a given stock symbol.
        """
        history_list = list()
        # Defining the variables link
        variables_url = self.financial_link_variables.format(self.symbol, period_1, period_2)

        # Performing a HTTP GET request to Yahoo's financial website
        response = requests.get(self.website_url + variables_url)

        # Parsing the extracted data to a BeautifulSoup object
        soup = BeautifulSoup(response.content, 'html.parser')
        historical_prices_table = soup.find("table", {"data-test": 'historical-prices'})

        # Getting all table's rows
        historical_prices_rows = historical_prices_table.find_all("tr")

        # Extracting the values from each row and structuring them
        for price_row in historical_prices_rows[1:-1]:
            stock_info = [price_column.text.replace(',', '') for price_column in price_row.find_all('span')]
            stock_info = {
                'symbol': self.symbol,
                'date': datetime.strptime(stock_info[0], '%b %d %Y'),
                'price_open': float(stock_info[1]),
                'price_high': float(stock_info[2]),
                'price_low': float(stock_info[3]),
                'price_close': float(stock_info[4]),
                'price_adj_close': float(stock_info[5]),
                'volume': float(stock_info[6])
            }
            history_list.append(Stock(**stock_info))

        self.stocks = Stocks(history=history_list)
        return self.stocks.history

    @exception_handler
    def export_as_json(self):
        """
        This method has the objective to create a JSON file and export the historical prices.
        """
        f = open("{}_historical_prices.json".format(self.symbol), "a")
        f.write(self.stocks.json())
        f.close()


# USAGE EXAMPLE
web_scraping = YahooFinancialWebScraping(symbol='AMZN')
date_1 = web_scraping.convert_date_to_timestamp('01/01/2021')
date_2 = web_scraping.convert_date_to_timestamp('01/31/2021')

hist_prices = web_scraping.extract_financial_data(period_1=date_1, period_2=date_2)
web_scraping.export_as_json()
