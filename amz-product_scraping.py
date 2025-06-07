from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests

def get_productTitle(soup):
    
    try:
        product_title = soup.find("span",attrs={'id':'productTitle'}).text.strip() #fetch's product title
    except AttributeError:
        product_title = "Error with Product title fetch"
        
    return product_title

def get_productPrice(soup):
    
    try:
        product_price = soup.find("span",attrs={'class':'a-price-symbol'}).text.strip() #fetch's product price
    except AttributeError:
        product_price = "Error with Product price fetch"
        
    return product_price

def get_productRating(soup):
    
    try:
        product_rating = soup.find("span",attrs={'id':'acrCustomerReviewText'}).text.strip() #fectch's product rating
    except AttributeError:
        product_rating = "Error with Product rating fetch"
        
    return product_rating

def get_productReview(soup):
    
    try:
        product_review = soup.find("span",attrs={'class':'a-size-base a-color-base'}).text.strip()
    except AttributeError:
        product_review = "Error with Product review fetch"
        
    return product_review

url = "https://www.amazon.in/s?k=phones&crid=286D7WELF89IT&sprefix=phones%2Caps%2C265&ref=nb_sb_noss_2"

HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

wpage = requests.get(url,headers=HEADERS)

print(wpage)

soup = BeautifulSoup(wpage.content,"html.parser")

links = soup.find_all("a", attrs = {'class':'a-link-normal s-line-clamp-2 s-link-style a-text-normal'})
#link = links[0].get('href')

links_arr = []
    
for link in links:
    links_arr.append(link.get('href'))
        
pdt = {"title":[], "price":[], "rating":[], "reviews":[]}
    
for link in links_arr:
    new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
        
    new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        
    pdt["title"].append(get_productTitle(new_soup))
    pdt["price"].append(get_productPrice(new_soup))
    pdt["rating"].append(get_productRating(new_soup))
    pdt["reviews"].append(get_productReview(new_soup))
    
    azp = pd.DataFrame.from_dict(pdt)
    azp['title'].replace('', np.nan, inplace=True)
    azp = azp.dropna(subset=['title'])
    azp.to_csv("amazon_product_details.csv", header=True, index=False)
    
    print(azp)


#prd_list = "https://www.amazon.com"+link

#new_wpage = requests.get(prd_list,headers=HEADERS)
#new_soup = BeautifulSoup(new_wpage.content,"html.parser")
#getting product title from the below line
#print(new_soup.find("span",attrs={'id':'productTitle'}))