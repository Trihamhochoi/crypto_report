from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pprint import pprint
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv(dotenv_path='../.env')

base_url = os.getenv('BASE_URL')  #'https://pro-api.coinmarketcap.com'
url = f'{base_url}/v1/cryptocurrency/map'
parameters = {
    'listing_status': 'active',
    'start': 1,
    'limit': 50,
    'symbol': 'PEPE,btc,wld,bnb',
    #'convert': 'USD',
    'sort': 'cmc_rank',
    'aux': "platform,first_historical_data,last_historical_data,is_active"
}
headers = {
    'Accepts': 'application/json',
    #'Accept-Encoding': 'deflate',
    'X-CMC_PRO_API_KEY': os.getenv("AUTH_KEY"),  #'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c'
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    print("Status code:",response.status_code)
    data = response.json()
    pprint(data)

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(response.text)
    print(e)
except Exception as e:
    print(response.text)
else:
    crypto_mapping = data['data']
    mapping_df = pd.json_normalize(data=crypto_mapping)
    mapping_df.to_csv(path_or_buf='../mapping_data.csv', index=False)
    print(mapping_df.to_string())