# # # # -------------------------------------------------------------------------------- # # # #
"""
This is the official python library for Ramzinex.com Cryptocurrency Exchange
Author: Mohammadreza Mirzaei
Email: mirzaeimohammadreza98@gmail.com
LinkedIn: https://www.linkedin.com/in/mohammad-reza-mirzaei/
"""
# # # # -------------------------------------------------------------------------------- # # # #
import json
from venv import logger
import pandas as pd
from datetime import datetime
import cloudscraper


# # # # -------------------------------------------------------------------------------- # # # #


class Client:
    """
    This is the official python library for Ramzinex.com Cryptocurrency Exchange
    Author: Mohammadreza Mirzaei
    Email: mirzaeimohammadreza98@gmail.com
    LinkedIn: https://www.linkedin.com/in/mohammad-reza-mirzaei/
    """

    def __init__(self, api=None):
        if api is not None:
            self.api = api  # client Ramzinex API
        else:
            pass
        self.scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
        self.response_ramzinex = None

    # # # # -------------------------------------------------------------------------------- # # # #
    # # # # Public API
    # # # # -------------------------------------------------------------------------------- # # # #

    def get_prices(self):
        try:
            url = "https://publicapi.ramzinex.com/exchange/api/exchange/prices"
            self.response_ramzinex = self.scraper.get(url)
            check_response_ramzinex = json.loads(self.response_ramzinex.text)
            return check_response_ramzinex
        except Exception as e:
            return Client.error_result(self, e=e, fname="get_prices", response=self.response_ramzinex)

    def get_markets(self, pair_id=None):
        try:
            url = "https://publicapi.ramzinex.com/exchange/api/v1.0/exchange/pairs"
            if pair_id is not None:
                url += "/" + str(pair_id)
            self.response_ramzinex = self.scraper.get(url)
            check_response_ramzinex = json.loads(self.response_ramzinex.text)
            return check_response_ramzinex
        except Exception as e:
            return Client.error_result(self, e=e, fname="get_markets", response=self.response_ramzinex)

    def get_markets_turnover(self):
        data = Client.get_markets()
        if data is not None:
            try:
                pairs_volume, usdt_pairs_volume, irr_pairs_volume = [], [], []
                for market in data["data"]:
                    try:
                        pair_dict = {"pair": market['tv_symbol']['ramzinex'],
                                     "quote_volume": str(market["financial"]["last24h"]['quote_volume']),
                                     "base_volume": str(market["financial"]["last24h"]['base_volume']),
                                     "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                        pairs_volume.append(pair_dict)
                        if market['tv_symbol']['ramzinex'][-3:] == "irr":
                            irr_pairs_volume.append(pair_dict)
                        elif market['tv_symbol']['ramzinex'][-4:] == "usdt":
                            usdt_pairs_volume.append(pair_dict)
                    except Exception as e:
                        logger.exception(str(e))

                # df = pd.DataFrame(pairs_volume)
                df_irr = pd.DataFrame(irr_pairs_volume)
                irr_markets_turnover = df_irr[['quote_volume']].astype(float).sum()['quote_volume']
                df_usdt = pd.DataFrame(usdt_pairs_volume)
                usdt_markets_turnover = df_usdt[['quote_volume']].astype(float).sum()['quote_volume']

                result_data = {"irr_markets_turnover": irr_markets_turnover,
                               "usdt_markets_turnover": usdt_markets_turnover,
                               "pairs_volume": pairs_volume,
                               "irr_pairs_volume": irr_pairs_volume,
                               "usdt_pairs_volume": usdt_pairs_volume
                               }
                result = {"status": 0, "message": "ok", "data": result_data}
                return result
            except Exception as e:
                return Client.error_result(self, e=e, fname="get_markets_turnover")

    def get_orderbook(self, pair_id, side):  # get ramzinex orderbook for pair
        print(self)
        url = "https://publicapi.ramzinex.com/exchange/api/v1.0/exchange/orderbooks/"
        try:
            if side == "sells":
                url += str(pair_id) + "/sells?readable=0&reverse=1"
            elif side == "buys":
                url += str(pair_id) + "/buys?readable=0"
            self.response_ramzinex = self.scraper.get(url=url)
            orderbook_ramzinex = json.loads(self.response_ramzinex.text)
            return orderbook_ramzinex
        except Exception as e:
            return Client.error_result(self, e=e, fname="get_orderbook", response=self.response_ramzinex)

    # # # # -------------------------------------------------------------------------------- # # # #
    # # # # Private API
    # # # # -------------------------------------------------------------------------------- # # # #

    # # # # -------------------------------------------------------------------------------- # # # #
    # # # # Others
    # # # # -------------------------------------------------------------------------------- # # # #

    def error_result(self, e, fname, response=None):
        try:
            logger.exception(str(e))
            err = "#error #" + fname
            if response is not None:
                err += "\nstatus_code:\n" + str(response.status_code) + \
                       "\nreason:\n" + str(response.reason)
            err += "\n" + str(e)
            result = {"status": -1, "error": err, "data": None}
            return result
        except:
            result = {"status": -1, "error": "Unknown Error", "data": None}
            return result
