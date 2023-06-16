import streamlit as st
from spare_parts import *

# main app


with st.sidebar:
    st.write("Amazon Scraper")
    # collapasable sidebar
    st.header("Instruction")
    with st.expander("How to use", expanded=True):  # hetre instruction will come
        st.write("""[1] Enter the name of the product that you want to search for. \n
[2] Click on the "Search" button. \n
[3] The system will start to scrape the Amazon website for the product details. \n
[4] The system may take a few minutes to complete the scraping process.\n
[5] Once the scraping process is complete, the product details will be displayed on the screen. \n
[6] If the system does not find any product details for the product that you entered, you will be prompted to start the process again""")


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
    else:
        st.write("please enter the product name")