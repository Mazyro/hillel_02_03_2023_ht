import requests
from requests import RequestException, HTTPError
import logging

"""сюдa пийдте название файла, и логер будет называться get base client"""
logger = logging.getLogger(__name__)


class APIBaseClient():
    base_url = ''

    def __init__(self):
        self.response = None

    def _request(self, method, url=None, **kwargs):
        try:
            self.response = requests.request(
                method=method,
                url=url or self.base_url,
                **kwargs
            )
        except (RequestException, HTTPError) as err:
            logger.error(err)

    #  этот метод должен быть в классе, от которого наследумся
    def prepare_data(self):
        raise NotImplementedError

    # метод должен только парсить, отказались
    # def save_data(self):
    #     raise NotImplementedError
