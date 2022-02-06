from nsetools import Nse
from dbo import getAllRows, insert, updateInstruments
import requests
import json

getIndicesJsonUrl = lambda underlying: f"https://www.nseindia.com/api/option-chain-indices?symbol={underlying}"

INDICES = ['NIFTY']
class Batch:

    def __init__(self, updateEquityPrices=True, updateIdxOptionPrices=True):
        symbolRows = getAllRows('pbt.t_symbols')
        instrumentRows = getAllRows('pbt.t_instruments')
        self.savedSymbols = {row[1]:row for row in symbolRows}
        self.savedInstruments = {row[2]:row for row in instrumentRows}
        if updateEquityPrices:
            self.allStocks, self.tradesInfo = self.getLiveEquityData()
        if updateIdxOptionPrices:
            self.updateIndexOptionPrices()

    def updateIndexOptionPrices(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36','Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'en-US,en;q=0.9,hi;q=0.8'}
        for index in INDICES:
            response = requests.get(getIndicesJsonUrl(index), headers = headers)
            if response.status_code==200:
                data = json.loads(response.text)
            else:
                print('Received error while getting data for : %s, Error : %s' % (index,response.status_code))

    def updateSymbols(self):
        values = []
        for symbol in self.allStocks:
            if (symbol not in self.savedSymbols.keys()) and self.tradesInfo.get(symbol):
                values.append(
                    (
                        self.tradesInfo.get(symbol).get('symbol'),
                        self.tradesInfo.get(symbol).get('companyName'),
                        'E',
                    )
                )
        print(values)
        insert(
            'pbt.t_symbols', 
            "(SYMBOL, S_NAME, S_TYPE)", 
            values,
            """(%s, %s, %s)"""
            )
        symbolRows = getAllRows('pbt.t_symbols')
        self.savedSymbols = {row[1]:row for row in symbolRows}


    def updateInstruments(self):
        instrumentsToUpdate = []
        instrumentsToInsert = []
        instruments = self.savedInstruments.keys()
        for symbol in self.savedSymbols:
            if symbol in instruments and symbol in self.tradesInfo.keys():
                instrumentsToUpdate.append([
                    self.tradesInfo.get(symbol).get('lastPrice'),
                    self.tradesInfo.get(symbol).get('pChange'),
                    self.savedSymbols.get(symbol)[0]
                ])
            elif symbol in self.tradesInfo.keys():
                instrumentsToInsert.append(
                    (
                        self.savedSymbols.get(symbol)[0],
                        symbol,
                        'E',
                        None,
                        None,
                        None,
                        None,
                        self.tradesInfo.get(symbol).get('lastPrice'),
                        self.tradesInfo.get(symbol).get('pChange'),
                    )
                )
        if instrumentsToInsert:
            insert(
                'pbt.t_instruments', 
                "(SYMBOL_ID,SYMBOL,INS_TYPE,DER_TYPE,STRIKEPRICE,EXPIRY,LOT_SIZE,LTP,CHANGEPER)", 
                instrumentsToInsert,
                """(%s, %s, %s,%s, %s, %s,%s, %s, %s)"""
            )
        for item in instrumentsToUpdate:
            updateInstruments(item[0],item[1],item[2])


    def getLiveEquityData(self):
        nse = Nse()
        allStocks = nse.get_stock_codes() 
        data = {}
        for item, val in allStocks.items():
            try:
                if item:
                    itemdata = nse.get_quote(item.strip())
                    if itemdata:
                        data[item.strip()] = {
                                    'symbol' : itemdata.get('symbol'),
                                    'companyName' : itemdata.get('companyName'),
                                    'lastPrice' : itemdata.get('lastPrice'),
                                    'pChange' : itemdata.get('pChange'),
                                }
                    print('Finished for stock %s' % item)
            except Exception as e:
                print('Failed to collect data for stock %s' % item)
                print('Error is %s' % e)
        return allStocks, data

if __name__=="__main__":
    bat = Batch(
        updateEquityPrices=False,
        updateIdxOptionPrices=True
    )
    # bat.updateSymbols()
    # bat.updateInstruments()