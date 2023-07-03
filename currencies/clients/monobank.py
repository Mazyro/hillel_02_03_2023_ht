from project.api_base_client import APIBaseClient


class MonoBank(APIBaseClient):
    base_url = 'https://api.monobank.ua/bank/currency'
    results = []
    """
    [{"currencyCodeA":840,"currencyCodeB":980,"date":1683064874,"rateBuy":36.65,"rateCross":0,"rateSell":37.4406},
    {"currencyCodeA":978,"currencyCodeB":980,"date":1683132374,"rateBuy":40.45,"rateCross":0,"rateSell":41.6008},]
    codes: USD = 840; EUR = 978; UAH = 980
    output
    [{'code': 'EUR', buy":"40.45","sale":"41.6008"},    ...
    ]
    """
    def prepare_data(self):
        self._request('get')
        self.results = []
        if self.response:
            for i in self.response.json()[:2]:
                if i['currencyCodeA'] == 840:
                    i['currencyCodeA'] = 'USD'
                elif i['currencyCodeA'] == 978:
                    i['currencyCodeA'] = 'EUR'

                self.results.append({
                    'code': i['currencyCodeA'],
                    'buy': i['rateBuy'],
                    'sale': i['rateSell']
                })


monobank_client = MonoBank()
