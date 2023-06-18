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
    max_retries = 10  # Maximum number of retries
    
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

            if response.status_code == 200: #type: ignore
                bsObj = BeautifulSoup(response.content, "html.parser")  #type: ignore
                for i in bsObj.findAll("div", {"class": "a-section a-spacing-small puis-padding-left-small puis-padding-right-small"}):
                    raw_list.append(i.text)

                time.sleep(np.random.randint(1, 10))
                alfa += 1
            else:
                print("Failed to fetch the page:", response.status_code)  #type: ignore
                break  # Break the main loop if the request fails continuously
        except Exception as e:
            print("Error:", e)
            break  # Break the main loop in case of any other exception

    for alfa in raw_list:
        try:
            target_string = alfa.split("out")
            net_rating = target_string[0].split(' ')[-2]

            if len(net_rating) > 3:
                net_rating = net_rating[-3:]

            title_name = target_string[0].split(' ')[0:-2]
            title_name = " ".join(title_name)

            total_rating = target_string[1].split("stars")
            rating_number = total_rating[1].split(" ")[1]
            price =  total_rating[1].split(" ")[3].split("₹")[1]
            #print([title_name, float(net_rating), int(rating_number.replace(",", "")), float(price.replace(",", ""))])
            final_list.append([title_name, float(net_rating), int(rating_number.replace(",", "")), float(price.replace(",", ""))])
        except:
            print("Error while processing the data")

    return pd.DataFrame(final_list, columns=["product name", "net_rating", "rating_number", "price[in Rs.]"])