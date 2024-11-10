from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pprint import pprint
from dotenv import load_dotenv
import os
import pandas as pd
import traceback
import sys
from openpyxl import load_workbook

class CoinmarketcapAPI:
    def __init__(self,file_env='.env'):
        load_dotenv(dotenv_path=file_env)
        self.auth_token = os.getenv('AUTH_KEY')
        self.base_url = os.getenv('BASE_URL')
        self.session = Session()
        headers = {
            'Accepts': 'application/json',
            # 'Accept-Encoding': 'deflate',
            'X-CMC_PRO_API_KEY': os.getenv("AUTH_KEY"),
        }
        self.session.headers.update(headers)
    def get_mapping_data(self,list_coin:list=['BTC','ETH']) -> pd.DataFrame:
        url = f'{self.base_url}/v1/cryptocurrency/map'
        list_coin_str = ','.join([i.upper() for i in list_coin])
        parameters = {
            'listing_status': 'active',
            'start': 1,
            'limit': 50,
            'symbol': list_coin_str,
            # 'convert': 'USD',
            'sort': 'cmc_rank',
            'aux': "platform,first_historical_data,last_historical_data,is_active"}
        try:
            response = self.session.get(url, params=parameters)
            print("Status code:", response.status_code)
            data = response.json()

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(response.text)
            print(e)
        except Exception as e:
            # Get Exception info
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            content = {'Title': '500_SERVER_ERROR',
                       'Type': str(exc_type),
                       'Detail': f'There is {type(e).__name__}: {e}',
                       "Filename": f_name,
                       "Exception": str(exc_obj),
                       'line_error': exc_tb.tb_lineno,
                       'traceback': traceback.format_exc()}
            print(traceback.format_exc())
            raise content
        else:
            crypto_mapping = data['data']
            mapping_df = pd.json_normalize(data=crypto_mapping)
            mapping_df = mapping_df[mapping_df['rank'] <= 1000].reset_index(drop=True)
            feat = ['id','rank','name','symbol','slug','is_active']
            #mapping_df.to_csv(path_or_buf='./mapping_data.csv', index=False)
            print(mapping_df[feat].to_string())
            return mapping_df[feat]

    # Get listing price data
    def get_market_data(self,
                        list_coin:list=['BTC','ETH'],
                        start:int=1,
                        limit:int=100,
                        destination_excel_path:str='Data/The-Jungle.xlsx')-> pd.DataFrame:
        # Get ID of cryptocurrency symbol
        df_symbol = self.get_mapping_data(list_coin)
        # get ID:
        coin_id_list = df_symbol['id'].values.tolist()
        url = f'{self.base_url}/v1/cryptocurrency/listings/latest'
        parameters = {
            'start': start,
            'limit': limit,
            'convert': 'USD',
        }
        try:
            response = self.session.get(url, params=parameters)
            print("Status code:", response.status_code)
            data = response.json()

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(response.text)
            print(e)
        except Exception as e:
            # Get Exception info
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            content = {'Title': '500_SERVER_ERROR',
                       'Type': str(exc_type),
                       'Detail': f'There is {type(e).__name__}: {e}',
                       "Filename": f_name,
                       "Exception": str(exc_obj),
                       'line_error': exc_tb.tb_lineno,
                       'traceback': traceback.format_exc()}
            print(traceback.format_exc())
            raise content
        else:
            crypto_data = data['data']
            data_final = []
            for crypto in crypto_data:
                if crypto['id'] in coin_id_list:
                    data_final.append(crypto)

            # Transform to dataframe
            price_df = pd.json_normalize(data=data_final).drop(columns='tags')
            feat = ['cmc_rank','id','name','symbol','date_added','circulating_supply','last_updated','quote.USD.price']
            print(price_df[feat].to_string())

            # Create excel writer
            # book = load_workbook(destination_excel_path)
            # writer = pd.ExcelWriter(destination_excel_path, engine='openpyxl')
            # # writer.book = book
            # writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
            # pprint(writer.sheets)

            # Save cmc price to existed excel file
            with pd.ExcelWriter(path=destination_excel_path, engine='openpyxl', mode='a',if_sheet_exists='replace') as writer:
                price_df[feat].to_excel(excel_writer=writer,
                                        sheet_name='CMC_price',
                                        index=False,
                                        float_format="%.6f")
            return price_df[feat]


if __name__ == '__main__':
    list_coin = ['BTC', 'ETH', 'near', 'jup', 'sol','dogs','wld']
    dest_path = 'Data/The-Jungle-test.xlsx'

    # CMC API
    cmc = CoinmarketcapAPI()
    #df_mapping = cmc.get_mapping_data(list_coin=['BTC','ETH','near','jup','sol'])
    df_price = cmc.get_market_data(list_coin,destination_excel_path=dest_path)