# '/v1/cryptocurrency/map'
parameters = {
    'listing_status': 'active',
    'start': 1,
    'limit': 50,
    'symbol': 'PEPE',
    'convert': 'USD',
    'sort': 'cmc_rank',
    'aux': "platform,first_historical_data,last_historical_data,is_active"
}

# Response
pepe = {'first_historical_data': '2023-04-17T06:40:00.000Z',
        'id': 24478,
        'is_active': 1,
        'last_historical_data': '2024-11-08T06:15:00.000Z',
        'name': 'Pepe',
        'platform': {'id': 1,
                     'name': 'Ethereum',
                     'slug': 'ethereum',
                     'symbol': 'ETH',
                     'token_address': '0x6982508145454ce325ddbe47a25d4ec3d2311933'},
        'rank': 24,
        'slug': 'pepe',
        'symbol': 'PEPE'}
