
import pandas as pd
import yfinance_download
import streamlit as st
import plotly.express as px

@st.cache_data
def load_dataframe():
    df = yfinance_download.load_records('^GSPC')
    return df

df = load_dataframe()

df = df.reset_index()

df = df[['Date', 'Close']]

df['year'] = df['Date'].dt.year

# ----------------------------------------------------------------------
tbl = pd.DataFrame()

for year in df['year'].unique():
    start_date = f'{year}-01-01'
    end_date   = f'{year + 10}-01-01'
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] < end_date)]

    filtered_df = filtered_df.reset_index()

    tbl[year] = filtered_df['Close']

years = df['year'].unique()

selected_years = st.sidebar.multiselect(label='Years', options=years, default=[2010, 2011, 2012, 2013, 2014])

# tbl = tbl[[2000, 2001, 2002, 2003, 2004]]

tbl = tbl[selected_years]

initial_values = tbl.iloc[0]

tbl_pct_chg = tbl.apply(lambda elt: (elt - initial_values[elt.name]) / initial_values[elt.name] * 100)

fig = px.line(tbl_pct_chg)

st.plotly_chart(fig)