from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests

# url = "https://www.flipkart.com/search?q=phones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

# link = links[0].get('href')

# prd_list = "https://www.flipkart.com"+link

# new_wpage = requests.get(prd_list,headers=HEADERS)
# new_soup = BeautifulSoup(new_wpage.content,"html.parser")

# pd_title = new_soup.find("span",attrs={'class':'VU-ZEz'}).text.strip()
# print(pd_title)

# pd_price = new_soup.find("div",attrs={'class':'Nx9bqj CxhGGd'}).text.strip()
# print(pd_price)

# pd_rating = new_soup.find("div",attrs={'class':'XQDdHH'}).text.strip()
# print(pd_rating)

# pd_reviews = new_soup.find("span",attrs={'class':'hG7V+4'}).next_sibling.text.strip()
# print(pd_reviews)

def get_productTitle(soup):
    
    try:
        product_title = soup.find("span",attrs={'class':'VU-ZEz'}).text.strip() #fetch's product title
    except AttributeError:
        product_title = "Error with Product title fetch"
        
    return product_title

def get_productPrice(soup):
    
    try:
        product_price = soup.find("div",attrs={'class':'Nx9bqj CxhGGd'}).text.strip() #fetch's product price
    except AttributeError:
        product_price = "Error with Product price fetch"
        
    return product_price

def get_productRating(soup):
    
    try:
        product_rating = soup.find("div",attrs={'class':'XQDdHH'}).text.strip() #fectch's product rating
    except AttributeError:
        product_rating = "Error with Product rating fetch"
        
    return product_rating

def get_productReview(soup):
    
    try:
        product_review = soup.find("span",attrs={'class':'hG7V+4'}).next_sibling.text.strip()
    except AttributeError:
        product_review = "Error with Product review fetch"
        
    return product_review

if __name__ == '__main__':
    
    url = "https://www.flipkart.com/search?q=phones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    
    wpage = requests.get(url,headers=HEADERS)
    
    soup = BeautifulSoup(wpage.content,"html.parser")
    
    links = soup.find_all("a", attrs = {'rel':'noopener noreferrer'})
    
    links_arr = []
    
    for link in links:
        links_arr.append(link.get('href'))
        
    pdt = {"title":[], "price":[], "rating":[], "reviews":[]}
    
    for link in links_arr:
        new_webpage = requests.get("https://www.flipkart.com" + link, headers=HEADERS)
        
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        
        pdt["title"].append(get_productTitle(new_soup))
        pdt["price"].append(get_productPrice(new_soup))
        pdt["rating"].append(get_productRating(new_soup))
        pdt["reviews"].append(get_productReview(new_soup))
    
    flp = pd.DataFrame.from_dict(pdt)
    flp['title'].replace('', np.nan, inplace=True)
    flp = flp.dropna(subset=['title'])
    flp.to_csv("filpkart_prduct_details.csv", header=True, index=False)
    
    print(flp)
    