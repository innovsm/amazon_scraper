import streamlit as st
from spare_parts import *

# main app


with st.sidebar:
    st.write("Amazon Scraper")
    # collapasable sidebar
    st.header("Instruction")
    with st.expander("How to use", expanded=True):  # hetre instruction will come
        st.write("hello anshu")


# getting input
data_1 = st.text_input("enter the product name")
button_1 = st.button("Run")


if(button_1):
    if(len(data_1) != 0):
        for i in range(10):
            alfa = scrape_amazon_data(data_1)
            if(len(alfa) != 0):
                break
        
        st.write(alfa)
        download_button = st.download_button('Download DataFrame as CSV', data=alfa.to_csv(), file_name='dataframe.csv')

