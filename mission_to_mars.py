#!/usr/bin/env python
# coding: utf-8

# Mission_to_Mars 

# # Load Dependencies

# In[16]:


# Dependencies
import os
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint


# # Set url variable

# In[2]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/'


# # Request and set response variable

# In[3]:


# Retrieve page with the requests module
response = requests.get(url)


# # Match response to html_string template variable

# In[4]:


html_string = response


# # Parse html_string with bs

# In[5]:


# Create BeautifulSoup object; parse with 'html.parser'
html_string = bs(response.text, 'html.parser')
print(html_string)


# 
# # Invoke splinter

# In[9]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[10]:


url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[11]:


# collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

# ```python
# # Example:
# news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"

# news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."
# ```

html = browser.html
soup = bs(html, 'html.parser')

nasa_t = soup.find("div",class_="content_title").text
nasa_p = soup.find("div", class_="article_teaser_body").text #*****Paragraph Text??**********

print(nasa_t)
print(nasa_p)


# In[ ]:





# In[13]:


### JPL Mars Space Images - Featured Image

# * Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).

# * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.

# * Make sure to find the image url to the full size `.jpg` image.

# * Make sure to save a complete url string for this image.

# ```python
# Example:
# featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

html = browser.html
soup = bs(html, 'html.parser')

main_url = 'https://www.jpl.nasa.gov'
img_url = soup.find("a", class_='button fancybox')["data-fancybox-href"]
featured_image_url = main_url + img_url

print(featured_image_url)




# In[14]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

twitter_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(twitter_url)

html = browser.html
soup = bs(html, 'html.parser')

mars_weather = soup.find('p', class_ = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
print(mars_weather)


# In[17]:


table_url = 'https://space-facts.com/mars/'
mars_table = pd.read_html(table_url)

mars_df = mars_table[1]
mars_df.columns = ['Mars Planet Profile', '']
mars_df.set_index('Mars Planet Profile', inplace=True)

mars_html_table = mars_df.to_html()
mars_html_table = mars_html_table.replace('\n', '')

print(mars_df)
print('-------------------------------------------------------------------------------------------------------------------')
pprint(mars_html_table)


# In[19]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemi_url)

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

