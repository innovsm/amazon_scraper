import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import pandas as pd

headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

headers_2 = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
def scrape_amazon_data(product):
    raw_list = []
    final_list = []
    alfa = 1
    product = product.replace(" ", "+")
    max_retries = 3  # Maximum number of retries
    
    while len(raw_list) < 300:
        try:
            if alfa == 1:
                url = "https://www.amazon.in/s?k={}".format(product)
            else:
                url = "https://www.amazon.in/s?k={}&page={}".format(product, alfa)

            # Retry the request multiple times in case of 503 error
            for _ in range(max_retries):
                response = requests.get(url,headers=headers_2, timeout=10)
                if response.status_code == 200:
                    break  # Break the retry loop if the request is successful
                else:
                    print("Retrying...")

            if response.status_code == 200:
                bsObj = BeautifulSoup(response.content, "html.parser")
                for i in bsObj.findAll("div", {"class": "a-section a-spacing-base"}):
                    data_1 = i.find("div", {"class": "a-section a-spacing-small puis-padding-left-small puis-padding-right-small"}).find("div", {"class": "a-section a-spacing-none a-spacing-top-small s-title-instructions-style"}).find("a")
                    if(data_1 != None):
                         asin = data_1.attrs["href"].split("/")[3]
                         #print(asin)
                    else:
                        asin = ""
                    
                    raw_list.append([asin,i.text,data_1.attrs['href']])
                # setting link


                time.sleep(np.random.randint(1, 10))
                alfa += 1
            else:
                print("Failed to fetch the page:", response.status_code)
                break  # Break the main loop if the request fails continuously
        except Exception as e:
            print("Error:", e)
            break  # Break the main loop in case of any other exception

    for alfa in raw_list:
        try:
            target_string = alfa[1].split("out")
            net_rating = target_string[0].split(' ')[-2]

            if len(net_rating) > 3:
                net_rating = net_rating[-3:]

            title_name = target_string[0].split(' ')[0:-2]
            title_name = " ".join(title_name)

            total_rating = target_string[1].split("stars")
            rating_number = total_rating[1].split(" ")[1]
            price =  total_rating[1].split(" ")[3].split("₹")[1]
            # getting discount
            target_string = alfa[1].split("(")

            temp_string_1 = ""
            for i in target_string[-1]:
                if i.isdigit():
                    temp_string_1 += i
                else:
                    break
            if(len(temp_string_1) != 0):
                discount_rate = int(temp_string_1)
            else:
                discount_rate = 0
            
            # getting price before discount
            price_before_discount = float(alfa[1].split("₹")[3].replace(",", ""))



            final_list.append(["https://www.amazon.in"+alfa[2],price_before_discount,discount_rate,alfa[0],title_name, float(net_rating), int(rating_number.replace(",", "")), float(price.replace(",", ""))])
        except:
            print("Error while processing the data")

    return pd.DataFrame(final_list, columns=['product_link',"price_before_discount","discount",'asin',"title", "net_rating", "rating_number", "price"])