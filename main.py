import streamlit as st
import pathlib
import pandas as pd
import json
import yfinance as yf
import altair as alt

st.title('BioRadish')

st.sidebar.write('''
# 日経バイオ系企業株価
こちらは株価可視化ツールです。
以下のオプションから表示日数を指定できます。
''')

st.sidebar.write('''
## 表示日数選択
''')

days = st.sidebar.slider('日数', 1, 100, 50)

st.write(f'''
### 過去 **{days}日間** の日経バイオ企業の株価
''')

@st.cache
def getStockPrice(tickers_dict, days):
    df = pd.DataFrame()
    for k,v in tickers_dict.items():
        stock = yf.Ticker(f'{k}.T').history(period=f'{days}d')
        stock.index = stock.index.strftime('%d %B %Y')
        stock = stock[['Close']].rename(columns={'Close': v[0]})
        stock = stock.T
        stock.index.name = 'Name'
        df = pd.concat([df, stock])
    return df

try: 
    st.sidebar.write('''
    ## 株価の範囲指定
    ''')
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 10000.0, (0.0, 10000.0)
    )
    
    #jsonの読み込み
    tickers_dict = json.load(open('ticker.json', 'r'))
    tickers_dict.pop('4365')
    df = getStockPrice(tickers_dict, days)
    companies = st.multiselect(
        '会社名を選択してください。',
        list(df.index),
        ['カイオム・バイオサイエンス']
    )

    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        data = df.loc[companies]
        st.write('### 株価 (JPY)', data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(JPY)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x='Date:T',
                y=alt.Y('Stock Prices(JPY):Q', stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        'おっと！なにかエラーが起きているようです。'
    )