import streamlit as st
from spare_parts import *

# main app


with st.sidebar:
    st.write("Amazon Scraper")
    # collapasable sidebar
    st.header("Instruction")
    with st.expander("How to use", expanded=True):  # hetre instruction will come
        st.write("""[1] Enter the name of the product that you want to search for. \n
[2] Click on the "Run" button. \n
[3] The system will start to scrape the Amazon website for the product details. \n
[4] The system may take a few minutes to complete the scraping process.\n
[5] Once the scraping process is complete, the product details will be displayed on the screen. \n
[6] If the system does not find any product details for the product that you entered, you will be prompted to start the process again \n
[7] If you are not satisfied with the results, you can click on the "Run Again" button to start the process again. \n""")


# getting input
data_1 = st.text_input("enter the product name")
button_1 = st.button("Run")

gama = None
if(button_1):
    if(len(data_1) != 0):
        for i in range(10):
            alfa = scrape_amazon_data(data_1)
            if(len(alfa) !=   0):
                gama = list(alfa['asin'])
                print(gama)
                break
        st.dataframe(alfa)
        download_button = st.download_button('Download DataFrame as CSV', data=alfa.to_csv(), file_name='{}.csv'.format(data_1))
        
       
    else:
        st.write("please enter the product name")

# ------------------
st.subheader("search additional product detail using ASIN")
data_2 = st.text_input("enter the ASIN number")
button_2 = st.button("asin_run")
if(button_2):
    if(len(data_2) != 0):
        try:

            for i in range(10):
                data_details ,data_review = create_dataframe(data_2)
                if(len(data_review) != 0):
                    break

            download_button_details = st.download_button("Download Technical Details", data_details.to_csv(), file_name = "{}_technical_detail.csv".format(data_2))
            download_button_review = st.download_button("Download Reviews", data_review.to_csv(), file_name = "{}_top_reviews.csv".format(data_2))
        except:
            st.write("please enter the valid ASIN number")