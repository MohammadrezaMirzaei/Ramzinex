import json
from venv import logger

# # # # -------------------------------------------------------------------------------- # # # #
import cloudscraper
scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# # # # -------------------------------------------------------------------------------- # # # #


class PublicAPI:
    """
    This is the official python library for Ramzinex.com Cryptocurrency Exchange
    Author: Mohammadreza Mirzaei
    Email: mirzaeimohammadreza98@gmail.com
    LinkedIn: https://www.linkedin.com/in/mohammad-reza-mirzaei/
    """

    def __init__(self):
        # self.api_ramzinex = api_ramzinex
        pass

    def get_markets(self, pair_id=None):
        # test
        response_ramzinex = None
        try:
            url = "https://publicapi.ramzinex.com/exchange/api/v1.0/exchange/pairs"
            if pair_id is not None:
                url += "/" + str(pair_id)
            response_ramzinex = scraper.get(url)
            check_response_ramzinex = json.loads(response_ramzinex.text)
            return check_response_ramzinex
        except Exception as e:
            logger.exception(str(e))
            err = "#error #get_markets"
            if response_ramzinex is not None:
                err += "\nstatus_code:\n" + str(response_ramzinex.status_code) + \
                       "\nreason:\n" + str(response_ramzinex.reason)
            err += "\n" + str(e)
            result = {"status": -1, "error": err, "data": None}
            return result
