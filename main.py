#https://en.wikipedia.org/wiki/Programmer

#Beginner Examples
"""import requests
from bs4 import BeautifulSoup

def get_page(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    #print(soup.a) #Returns the first anchor tag
    #print(soup.find_all("a")) #Grab all anchor tags, ".find" grabs the first one
    #print(soup.find(id="mw-searchButton"))# replace with any tag
    #print(soup.title.string)#Title of the Page in string

    tag = soup.find_all("a")

    for t in tag:
        url2 =t.get("href")
        print(url2)

get_page(input("What url would you like to scrape?\n "))"""

#-------------------------------------------------------------------------------------------

#Real Tool
#https://www.yahoo.com
import requests
from bs4 import BeautifulSoup
from urllib import *
from urllib.parse import urljoin


visited_urls = set() #No need to worry about duplicates

def spider_urls(url, keyword):
    try:
        response = requests.get(url)
    except:
        print(f"Request failed {url}")
        return

    if response.status_code==200:
        soup = BeautifulSoup(response.content, 'html.parser')

        a_tag = soup.find_all('a')
        urls=[]


        for tag in a_tag:
            href = tag.get("href")
            if href is not None and href !="":
                urls.append(href)
        #print(urls)


        for urls2 in urls: #Remove duplicates
            if urls2 not in visited_urls:
                visited_urls.add(url)
                url_join= urljoin(url,urls2)
                if keyword in url_join:
                    print(url_join)
                    spider_urls(url_join,keyword)
                else:
                    pass












url = input("Enter the URL you want to scrape. \n")
keyword = input("Enter the keyword to search for in The URL provided. ")
spider_urls(url,keyword)

