import streamlit as st
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import pandas as pd
from ta.momentum import RSIIndicator

dt_start = datetime.today()-timedelta(days=3600)
dt_end = datetime.today()

countries = ['France', 'United states']
intervals = ['Daily', 'Weekly', 'Monthly']

# Labels
country_select = st.sidebar.selectbox("Pays:", countries)
stock = ip.get_stocks_list(country=country_select)
stock_select = st.sidebar.selectbox("Action:", stock)
etf = ip.get_etfs_list(country=country_select)
etf_select = st.sidebar.selectbox("ETF:", etf)
from_date = st.sidebar.date_input('Début:', dt_start)
to_date = st.sidebar.date_input('Fin:', dt_end)
interval_select = st.sidebar.selectbox("Sélection de l'intervale:", intervals)
data_load = st.sidebar.checkbox('Détail')

# Comments
st.title('Shares Monitor')
st.markdown(" 🎲 @Thomas Roussel")
st.markdown(" Mise en pratique de Python")
st.header('')
st.subheader('')

# retrieve stock information
search_stock_result = ip.search_quotes(text=stock_select, countries=[country_select], n_results=1)
search_etf_result = ip.search_quotes(text=etf_select, countries=[country_select], n_results=1)

stock_symbol = search_stock_result.symbol
etf_name = search_etf_result.name

def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)

#@st.cache(allow_output_mutation=True)
def consulter_stock(stock, country, from_date, to_date, interval):
    df = ip.get_stock_historical_data(
        stock=stock, country=country, from_date=from_date,
        to_date=to_date, interval=interval)
    return df

#@st.cache(allow_output_mutation=True)
def consulter_etf(etf, country, from_date, to_date, interval):
    df = ip.get_etf_historical_data(
        etf=etf, country=country, from_date=from_date,
        to_date=to_date, interval=interval)
    return df

def plotCandleStick(df, actif='ticket'):
    trace = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': actif,
        'showlegend': False
    }

    data = [trace]
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    return fig

if from_date > to_date:
    st.sidebar.error('La date ne peut être supérieure à la date du jour')
else:
    df1 = consulter_stock(stock_symbol, country_select, format_date(
        from_date), format_date(to_date), interval_select)
    # Indicateur RSI
    df1["RSI"] = RSIIndicator(df1["Close"]).rsi().dropna()
    try:
        fig = plotCandleStick(df1)
        candle = st.plotly_chart(fig)
        line = st.line_chart(df1.Close)
        rsi = st.area_chart(df1.RSI)
        if data_load:
            st.subheader('Détail')
            data = st.dataframe(df1)
            stock_select = st.sidebar.selectbox
    except Exception as e:
        st.error(e)

    df2 = consulter_etf(etf_name, country_select, format_date(
        from_date), format_date(to_date), interval_select)
    try:
        fig = plotCandleStick(df2)
        candle = st.plotly_chart(fig)
        line = st.line_chart(df2.Close)
        if data_load:
            st.subheader('Détail')
            data = st.dataframe(df2)
            stock_select = st.sidebar.selectbox
    except Exception as e:
        st.error(e)
