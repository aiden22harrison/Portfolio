import requests
from xlsxwriter import workbook

# This class can get data from a coin and can write this data onto a sheet.


class coinGrabber:
    # This is a basic initiation. It requires an API key, the price you bought the coin, the coin you are looking at.
    # It also has the optional currency arguement.
    def __init__(self, api_key, coin, currency='USD') -> None:
        self.api_key = api_key
        self.coin = coin
        self.currency = currency

    # This finds the price of self.coin. It can also accept a Boolean for an optional arguement named Meta
    def currentPrice(self, meta=False) -> dict:
        data = {"currency": self.currency, "code": self.coin, "meta": meta}
        return requests.post('https://api.livecoinwatch.com/coins/single', json=data, headers={'content-type': 'application/json', 'x-api-key': self.api_key}).json()

    # This checks the status of the api
    def status(self) -> int:
        return requests.post('https://api.livecoinwatch.com/status').status_code


class coinsGrab:

    def __init__() -> None:
        pass
