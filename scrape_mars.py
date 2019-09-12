# !/usr/bin/env PythonData
# coding: utf-8

# scrape_mars

import os
import time

import pandas as pd

from bson import ObjectId  # For ObjectId to work
from decorator import append
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return  browser



def scrape():
    browser = init_browser()

    output_dict = {}


    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

  
    nasa_t = getattr(soup.find("div", class_="content_title"), 'text', None)
    nasa_p = getattr(soup.find("div", class_="article_teaser_body"), 'text',None)


    # nasa_t = soup.find("div", class_="content_title").text
    # # *****Paragraph Text??**********
    # nasa_p = soup.find("div", class_="article_teaser_body").text

    browser.quit()

    # print(nasa_t)
    # print(nasa_p)
    output_dict["nasa_t"] = nasa_t
    output_dict["nasa_p"] = nasa_p


    # **********************************************
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser = init_browser()

    browser.visit(url)

    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')

    time.sleep(1)

    main_url = 'https://www.jpl.nasa.gov'
    img_url = soup.find("a", class_='button fancybox')["data-fancybox-href"]
    featured_image_url = main_url + img_url

    output_dict["featured_image_url"] = featured_image_url
    browser.quit()

    # ***************************************
    # def scrape():
    #     browser = init_browser()
    # url = 'https://mars.nasa.gov/news/'
    # browser.visit(url)

    browser = init_browser()

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    time.sleep(2)

    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find(
        'p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    # print(mars_weather)
    output_dict["mars_weather"] = mars_weather
    browser.quit()

    # *************************************************************

    table_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(table_url)

    mars_df = mars_table[1]
    mars_df.columns = ['Mars Planet Profile', '']
    mars_df.set_index('Mars Planet Profile', inplace=True)
    time.sleep(1)
    
    mars_df = mars_df.replace('\n', '')
    time.sleep(1)
    mars_html_table = mars_df.to_html()

    # print(mars_df)
    # print('-------------------------------------------------------------------------------------------------------------------')
    # pprint(mars_html_table)

    output_dict["mars_df"] =  mars_df
    output_dict["mars_html_table"] = mars_html_table

    browser.quit()


# ******************************************************************************

    browser = init_browser()

    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)

    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemi_url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    stock_url = 'https://astrogeology.usgs.gov'
    img_links = soup.find_all('div', class_="item")
    hemisphere_image_urls = []

    for img in img_links:
        hemi = img.find('h3').text
        i_url = img.find('img', class_='thumb')['src']
        img_url = stock_url + i_url
        time.sleep(1)
        hemisphere_image_urls.append({"title": hemi, "img_url": img_url})
        time.sleep(1)
    output_dict["hemisphere_image_urls"] = hemisphere_image_urls
    # output_dict["report"] = build_report(hemisphere_image_urls)

    browser.quit()

    return output_dict

# helper function to build surf report
# def build_report(hemisphere_image_urls):
#     final_report = ""
#     for p in hemisphere_image_urls:
#         final_report += " " + p.get_text()
#         print(final_report)
#     return final_report
