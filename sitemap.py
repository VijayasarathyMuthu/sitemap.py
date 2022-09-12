import requests
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import json

url = "https://screenrant.com/sitemap.xml"

url = st.text_input ("Input the url of the sitemap of the website")


r = requests.get(url, headers={"User-Agent": "XY"})

with st.spinner(text="Fetching urls..."):
    with requests.Session() as req:
            r = requests.get(url, headers={"User-Agent": "XY"})
            soup = BeautifulSoup(r.content, 'html.parser')
            links = [item.text for item in soup.select("loc")]
            df_final = []
            links = links[0:2]
            for link in links:
                    link = link.strip()
                    res = requests.get(link, headers={"User-Agent": "XY"})
                    soup = BeautifulSoup(res.content, 'html.parser')
                    end = [item.text for item in soup.select("loc")]
                    lastmod = [item.text for item in soup.select("lastmod")]
                    zipped = dict(enumerate(zip(end, lastmod)))
                    df = pd.DataFrame.from_dict(zipped).T.rename(columns={0:"url",1:"Last_modified"})
                    df_final.append(df)
            df_final = pd.concat(df_final).reset_index().drop(columns=["index"])
            st.dataframe(df_final.sample(10))
st.success('Done!')

@st.cache
def convert_df(df_final):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df_final.to_csv().encode('utf-8')

csv = convert_df(df_final)

st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='large_df.csv',
     mime='text/csv',
 )