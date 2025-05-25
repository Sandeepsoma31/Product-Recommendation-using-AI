from bs4 import BeautifulSoup
import pandas as pd
import requests

url = "https://www.amazon.in/s?k=phones&crid=286D7WELF89IT&sprefix=phones%2Caps%2C265&ref=nb_sb_noss_2"

HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

wpage = requests.get(url,headers=HEADERS)

print(wpage)

soup = BeautifulSoup(wpage.content,"html.parser")

links = soup.find_all("a", attrs = {'class':'a-link-normal s-line-clamp-2 s-link-style a-text-normal'})
link = links[0].get('href')

prd_list = "https://www.amazon.com"+link

new_wpage = requests.get(prd_list,headers=HEADERS)
new_soup = BeautifulSoup(new_wpage.content,"html.parser")
print(new_soup.find("span",attrs={'id':'productTitle'}))