#!/usr/bin/env python3

import json
import logging
import requests

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

class Bisq:

    def getOffers(fiat, direction, refprice, session):

        # fiat = eur, usd,
        # direction = buy or sell
        # refprice = int
        # tor = 1 or 0

        bisqBaseUrlTor = 'http://bisqmktwih46lbda65e27uefnn2nznnk5oygdwyqcdrpo7yy7i5qd7ad.onion'

        bisqApi = f"{bisqBaseUrlTor}/api/offers?market=btc_{fiat.upper()}&direction={direction.upper()}"
        try:
            f = session.get(bisqApi)
        except requests.exceptions.Timeout as e:
            # Maybe set up for a retry, or continue in a retry loop
            logger.error("Error obtaining orders from Bisq (timeout): %s - %s" % (e.errno, e.strerror))
            return []
        except requests.exceptions.TooManyRedirects as e:
            logger.error("Error obtaining orders from Bisq (too many redirects): %s - %s" % (e.errno, e.strerror))
            return []
        except requests.exceptions.RequestException as e:
            logger.error("Error obtaining orders from Bisq: %s - %s" % (e.errno, e.strerror))
            return []
        try:
            values = f.json()
            f.close()
        except json.decoder.JSONDecodeError as e:
            logger.error("Error decoding orders from Bisq: %s - %s" % (e.errno, e.strerror))
            return []
        key = f"btc_{fiat}"

        alloffers = []

        for line in values[key][direction + 's' ]:
            offer = {}
            offer['exchange'] = 'Bisq'
            offer['price'] = int(float(line['price']))
            offer['dif'] = (offer['price']/refprice-1)*100
            offer['min_btc'] = float(line['min_amount'])
            offer['max_btc'] = float(line['amount'])
            offer['min_amount'] = int(offer['min_btc'] * offer['price'])
            offer['max_amount'] = int(float(line['volume']))
            offer['method'] = line['payment_method']
            alloffers.append(offer)
        alloffers.sort(key=lambda item: item.get('price'))
        return alloffers

    def getFiatPrice(fiat, session):
        bisqApi = 'http://ro7nv73awqs3ga2qtqeqawrjpbxwarsazznszvr6whv7tes5ehffopid.onion/getAllMarketPrices'
        try:
            f = session.get(bisqApi)
        except requests.exceptions.Timeout as e:
            # Maybe set up for a retry, or continue in a retry loop
            logger.error("Error obtaining price from Bisq (timeout): %s - %s" % (e.errno, e.strerror))
            return 1
        except requests.exceptions.TooManyRedirects as e:
            logger.error("Error obtaining price from Bisq (too many redirects): %s - %s" % (e.errno, e.strerror))
            return 1
        except requests.exceptions.RequestException as e:
            logger.error("Error obtaining price from Bisq: %s - %s" % (e.errno, e.strerror))
            return 1
            # * I return 1 instead of 0 to avoid errors raised dividing by the price

        try:
            priceapi = f.json()
            f.close()
        except json.decoder.JSONDecodeError as e:
            logger.error("Error decoding orders from Bisq: %s - %s" % (e.errno, e.strerror))
            return 1

        for currency in priceapi['data']:
            if (currency['currencyCode'].lower()==fiat):
                return int(float(currency['price']))
