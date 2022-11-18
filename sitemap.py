import streamlit as st
import pandas as pd
import advertools as adv

url = "https://screenrant.com/sitemap.xml"

url = st.text_input ("Input the url of the sitemap of the website")



with st.spinner('Fetching the data...'):
    sitemap = adv.sitemap_to_df(url, recursive=True )
st.success('Done!')

@st.cache
def convert_df(sitemap):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return sitemap.to_csv().encode('utf-8')

csv = convert_df(sitemap)
    
st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='large_df.csv',
     mime='text/csv',
 )
