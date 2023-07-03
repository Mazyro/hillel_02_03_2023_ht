from project.api_base_client import APIBaseClient


class NationBank(APIBaseClient):
    base_url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange'
    results = []

    """
    https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json
    [{ ..., "r030":840,"txt":"Долар США","rate":36.5686,
    "cc":"USD","exchangedate":"04.05.2023"}
     ...
    ,{"r030":978,"txt":"Євро","rate":40.3699,
    "cc":"EUR","exchangedate":"04.05.2023"} ... ]
    """

    def prepare_data(self):
        self._request(
            'get',
            params={
                'json': ''
            }
        )
        self.results = []
        if self.response:
            for i in self.response.json():
                if (i['r030'] == 840) or (i['r030'] == 978):
                    self.results.append({
                        'code': i['cc'],
                        'buy': i['rate'],
                        'sale': i['rate']
                    })


nationbank_client = NationBank()
