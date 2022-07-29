import pandas as pd
import json
import mojimoji

tosho = pd.read_excel('../data/stock.xls')

tosho = tosho.loc[
    (tosho['17業種区分'] == '医薬品 ')#|
    # (tosho['銘柄名'].str.contains('医薬'))|
    # (tosho['銘柄名'].str.contains('製薬'))
][[
    'コード',
    '銘柄名',
    '市場・商品区分',
]].rename(
    columns={
    'コード': 'ticker',
    '銘柄名' : 'company',
    '市場・商品区分' : 'market',
    }
)

tosho['company'] = tosho['company'].apply(mojimoji.zen_to_han,kana=False, digit=True, ascii=True)
tosho['market'] = tosho['market'].apply(mojimoji.zen_to_han,kana=False, digit=True, ascii=True)

tosho['list'] = tosho[['company', 'market']].values.tolist()
ticker_dict = dict(tosho[['ticker', 'list']].values)

json_path = '../json/ticker.json'
json_file = open(json_path, mode='w')

json.dump(ticker_dict, json_file, indent=2, ensure_ascii=False)
json_file.close()