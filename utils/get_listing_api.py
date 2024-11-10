from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pprint import pprint
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv(dotenv_path='../.env')

base_url = os.getenv('BASE_URL')  #'https://pro-api.coinmarketcap.com'
url = f'{base_url}/v1/cryptocurrency/listings/latest'
parameters = {
    'start': 1,
    'limit': 100,
    #'symbol': 'PEPE',
    'convert': 'USD',
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

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(response.text)
    print(e)
except Exception as e:
    print(response.text)
else:
    crypto_data = data['data']
    data_final = []
    for crypto in crypto_data:
        if crypto['id'] in [1,1839,24478,13502]:
            data_final.append(crypto)

    test_df = pd.json_normalize(data=data_final)
    test_df.to_csv(path_or_buf='../pepe_sample.csv', index=False)
    print(test_df.to_string())