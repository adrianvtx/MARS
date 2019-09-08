#!/usr/bin/env python
# coding: utf-8

# Mission_to_Mars 

# Dependencies
import os
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import requests
import time
from pprint import pprint


# URL of page to be scraped
# url = 'https://mars.nasa.gov/news/'

# Retrieve page with the requests module
# response = requests.get(url)


# # Match response to html_string template variable

# html_string = response


# # Parse html_string with bs

# Create BeautifulSoup object; parse with 'html.parser'
# html_string = bs(response.text, 'html.parser')
# print(html_string)



executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


def scrape():
# browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)


    html = browser.html
    soup = bs(html, 'html.parser')

    nasa_t = soup.find("div",class_="content_title").text
    nasa_p = soup.find("div", class_="article_teaser_body").text #*****Paragraph Text??**********

    # print(nasa_t)
    # print(nasa_p)

    # **********************************************
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    time.sleep(1)


    html = browser.html
    soup = bs(html, 'html.parser')

    time.sleep(1)


    main_url = 'https://www.jpl.nasa.gov'
    img_url = soup.find("a", class_='button fancybox')["data-fancybox-href"]
    featured_image_url = main_url + img_url

    # print(featured_image_url)

    # ***************************************
    # def scrape():
    #     browser = init_browser()
    # url = 'https://mars.nasa.gov/news/'
    # browser.visit(url)


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find('p', class_ = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    # print(mars_weather)


    table_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(table_url)

    mars_df = mars_table[1]
    mars_df.columns = ['Mars Planet Profile', '']
    mars_df.set_index('Mars Planet Profile', inplace=True)

    mars_html_table = mars_df.to_html()
    mars_html_table = mars_html_table.replace('\n', '')

    # print(mars_df)
    # print('-------------------------------------------------------------------------------------------------------------------')
    # pprint(mars_html_table)


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)


    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    stock_url = 'https://astrogeology.usgs.gov'
    img_links = soup.find_all('div', class_= "item")
    hemisphere_image_urls = []

    for img in img_links:
        hemi = img.find('h3').text
        i_url = img.find('img', class_='thumb')['src']
        img_url = stock_url + i_url
        hemisphere_image_urls.append({"title" : hemi, "img_url" : img_url})
        
    hemisphere_image_urls

    # hemisphere_image_urls = [
    #     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #     {"title": "Cerberus Hemisphere", "img_url": "..."},
    #     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    # ]

    mars_db = {  
        "nasaTitle": nasa_t,
        "nasaPgph": nasa_p,
        "featureImage": featured_image_url,
        "marsWeath": mars_weather,
        "marsInfo": mars_df,
        "marsTable": mars_html_table,
        "imageList": hemisphere_image_urls
        }

        # Close the browser after scraping
# browser.quit()

    # Return results
    return mars_db