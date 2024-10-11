
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

number_of_years = st.sidebar.number_input(label='Number of years', min_value=1, max_value=100, value=10)

# for year in df['year'].unique():
#     start_date = f'{year}-01-01'
#     end_date   = f'{year + 10}-01-01'
#     filtered_df = df[(df['Date'] >= start_date) & (df['Date'] < end_date)]

#     filtered_df = filtered_df.reset_index()

#     tbl[year] = filtered_df['Close']

for year in df['year'].unique():
    start_date = f'{year}-01-01'
    end_date   = f'{year + number_of_years}-01-01'
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] < end_date)]

    filtered_df = filtered_df.reset_index()

    tbl[year] = filtered_df['Close']


years = df['year'].unique()

selected_years = st.sidebar.multiselect(label='Years', options=years, default=[2010, 2011, 2012, 2013, 2014])

# tbl = tbl[[2000, 2001, 2002, 2003, 2004]]

# tbl = tbl[selected_years]

initial_values = tbl.iloc[0]

tbl_pct_chg = tbl.apply(lambda elt: (elt - initial_values[elt.name]) / initial_values[elt.name] * 100)

tmp = tbl_pct_chg.transpose()

tmp.iloc[:,0]

tmp = tmp.iloc[:,-1]

tmp[tmp < 0]

# tbl_pct_chg.max()

# tbl_pct_chg.max(axis=0)

# tbl_pct_chg.max(axis=1)

if st.sidebar.checkbox('Show max and min', value=False):

    tbl_pct_chg['max'] = tbl_pct_chg.max(axis=1)

    tbl_pct_chg['min'] = tbl_pct_chg.min(axis=1)

    selected_years = selected_years + ['max', 'min']

tbl_pct_chg = tbl_pct_chg[selected_years]

# tbl_pct_chg['max']



fig = px.line(tbl_pct_chg)

st.plotly_chart(fig)