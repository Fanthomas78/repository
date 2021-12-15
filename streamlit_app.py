import streamlit as st
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import pandas as pd
from ta.momentum import RSIIndicator

# retrieve stock information
text='evergrande'
search_result = ip.search_quotes(text=text, n_results=1)
print(search_result)
name=search_result.name
symbol=search_result.symbol
country=search_result.country
products=search_result.pair_type

dt_start = datetime.today()-timedelta(days=3600)
dt_end = datetime.today()

def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)

countries = ['France', 'United states']
intervals = ['Daily', 'Weekly', 'Monthly']

@st.cache(allow_output_mutation=True)
def consulter(stock, country, from_date, to_date, interval):
    df = ip.get_stock_historical_data(
        stock=stock, country=country, from_date=from_date,
        to_date=to_date, interval=interval)
    return df

def plotCandleStick(df, actif='ticket'):
    trace1 = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': actif,
        'showlegend': False
    }

    data = [trace1]
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    return fig

# Labels
country_select = st.sidebar.selectbox("Pays:", countries)
stock = ip.get_stocks_list(country=country_select)
stock_select = st.sidebar.selectbox("Actif:", stock)
from_date = st.sidebar.date_input('Début:', dt_start)
to_date = st.sidebar.date_input('Fin:', dt_end)
interval_select = st.sidebar.selectbox("Sélection de l'intervale:", intervals)
data_load = st.sidebar.checkbox('Détail')

# éléments de la page
st.title('Stock Monitor')
st.markdown(" 🎲 @Thomas Roussel")
st.markdown(" Mise en pratique de Python")
st.header('')
st.subheader('')

line = st.empty()
candle = st.empty()

if from_date > to_date:
    st.sidebar.error('La date ne peut être supérieure à la date du jour')
else:
    df = consulter(stock_select, country_select, format_date(
        from_date), format_date(to_date), interval_select)
    # Indicateur RSI
    df["RSI"] = RSIIndicator(df["Close"]).rsi().dropna()
    try:
        fig = plotCandleStick(df)
        candle = st.plotly_chart(fig)
        line = st.line_chart(df.Close)
        rsi = st.area_chart(df.RSI)
        if data_load:
            st.subheader('Détail')
            data = st.dataframe(df)
            stock_select = st.sidebar.selectbox
    except Exception as e:
        st.error(e)