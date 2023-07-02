from currencies.models import CurrencyHistory
from project.api_base_client import APIBaseClient


class PrivatBank(APIBaseClient):
    base_url = 'https://api.privatbank.ua/p24api/pubinfo'

    def _prepare_data(self) -> list:
        """
        [
            {"ccy":"EUR","base_ccy":"UAH","buy":"39.69520","sale":"41.32231"},
            {"ccy":"USD","base_ccy":"UAH","buy":"36.56860","sale":"37.45318"}
        ]
        return: dict
        [{"code": "USD", "buy":"39.69520","sale":"41.32231"},]
        """
        self._request(
            'get',
            params={
                'json': '',
                'exchange': '',
                'coursid': 5,
            }
        )
        results = []
        if self.response:
            for i in self.response.json():
                results.append({
                    'code': i['ccy'],
                    'buy': i['buy'],
                    'sale': i['sale'],
                })
        return results

    def save(self):
        results = []
        for i in self._prepare_data():
            results.append(
                CurrencyHistory(
                    **i  # список словарей
                )
            )
        if results:
            CurrencyHistory.objects.bulk_create(results)  # наполнили модель
        print('ok')


"""Импровизированный синглтон"""
privatbank_client = PrivatBank()
