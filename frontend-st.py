import plotly.graph_objects as go
import streamlit as st
import pandas as pd


@st.cache(hash_funcs={pd.DataFrame: lambda _: None}, suppress_st_warning=True)
def get_data():
    st.write("Cache refreshed, getting new data...")
    master_df = pd.read_csv("Master_df.csv", index_col=0)
    selection_list = master_df['Key'].unique().tolist()
    # Salah_df = pd.read_csv("Salah_sample_csv.csv", index_col=0)
    # Havertz_df = pd.read_csv("Havertz_sample_csv.csv", index_col=0)
    return master_df, selection_list

master_df, selection_list = get_data()
# fig = load_fig()
# master_df = download_sheet('Master')
st.header("FPL Price Track")
choice = st.selectbox(
    "Choose a player",
    selection_list
)
# lookup_dict = {'Salah': "Salah", "Havertz": "Havertz", "De Bruyne": "Choice 3"} for later implementations
df = master_df.loc[master_df['Key']==choice]
#if lookup_dict[choice] == 'Salah':
 #   df = Salah_df
#elif lookup_dict[choice] == 'Havertz':
 #   df = Havertz_df

df
df2 = df[['Points', 'Form', 'Cost', 'Date']].copy()
df2['Date'] = pd.to_datetime(df2['Date'], format='%Y-%m-%d %H:%M:%S.%f')
df2['Date'] = df2['Date'].dt.strftime('%y/%m/%d')
#df2.set_index('Date',inplace=True)
st.line_chart(df2[['Points', 'Form', 'Cost', 'Date']].set_index('Date'))
