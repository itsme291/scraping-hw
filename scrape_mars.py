#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

def scrape():
    # # NASA Mars News
    url = 'https://mars.nasa.gov/news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    title = soup.find('div', class_='content_title').text.strip()
    para = soup.find('div', class_='rollover_description_inner').text.strip()

    # # JPL Mars Space Images - Featured Image
    executable_path = {'executable_path': '/Users/saurabhgoyal/Downloads/chromedriver'}
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_url = soup.find('a', class_="button fancybox")['data-fancybox-href']
    image_url = 'https://www.jpl.nasa.gov' + image_url

    # # Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    tweets = soup.find_all('li', class_='js-stream-item')
    i = 0
    mars_weather = ""
    while 'Sol ' not in mars_weather:
        mars_weather = tweets[i].find('p', class_='TweetTextSize').text.strip()
        i=i+1

    # # Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Description', 'Data']
    df.set_index('Description', inplace=True)
    df.to_html('table.html')
    html_table = df.to_html()
    html_table.replace('\n', '')


    # # Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    results = soup.find_all('a', class_='itemLink')
    hemisphere_image_urls = []
    for result in results:
        title = result.h3.text
        url = 'https://astrogeology.usgs.gov' + result['href']
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        img_url = soup.find('div', class_='downloads').find('a')['href']
        hemisphere_image_urls.append({"title": title, "img_url": img_url})

    # # Create combine dict
    mars_data = {
        'latest_title': title,
        'latest_para': para,
        'image_url': image_url,
        'weather_tweet': mars_weather,
        'data_table': html_table,
        'hemispheres_dict': hemisphere_image_urls
    }
    return mars_data

