 #!/usr/bin/env python
# coding: utf-8

# In[55]:


# Import Dependencies
import os
import pandas as pd
from bs4 import BeautifulSoup 
from splinter import Browser 
from flask_pymongo import PyMongo
import pymongo
import requests
import time


# In[56]:


# Initialize PyMongo 
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[57]:


# Define database and collection
db = client.mars_db
collection = db.items


# In[58]:
def scrape():

    def init_browser():
        # @NOTE: Replace the path with your actual path to the chromedriver
        executable_path = {"executable_path": "chromedriver"}
        return Browser("chrome", **executable_path, headless=True)


    # In[59]:


    # Use requests and BeautifulSoup to scrape Nasa News for latest news
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    print(soup.prettify())


    # In[60]:


    results = soup.find('div', class_='features')
    print(results)


    # In[61]:


    #  collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    news_title = results.find('div', class_='content_title').text
    news_p = results.find('div', class_='rollover_description_inner').text

    print(news_title)
    print(news_p)


    # In[62]:


    #  Loop & collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    results = soup.find_all("div", class_='slide')
    # print(results)

    for result in results:
        
        title=result.find("div", class_='content_title')
        # print(title)
        
        paragraph=result.find("div", class_="rollover_description_inner")
        #print(paragraph)
        
        title_text = title.text
        #print(title_text)

        para_text = paragraph.text
        #print(para_text)


    # In[63]:


    # Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    # https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    # Make sure to find the image url to the full size `.jpg` image.
    # Make sure to save a complete url string for this image.
    # https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    #----------------------------------------------------------------
    # Initialize browser
    browser = init_browser()

    # Visit the page
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # featured_image_url
    #featured_image_url="https://www.jpl.nasa.gov"+soup.find("article")['style'].split("('", 1)[1].split("')")[0]
    # print(featured_image_url)
    featured_image = soup.find("li", class_="slide")
    featured_image_fragment = featured_image.find(class_="fancybox")['data-fancybox-href']

    base_url = "https://www.jpl.nasa.gov"

    featured_image_url = base_url + featured_image_fragment


    # In[64]:


    #* Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
    # Initialize browser
    browser = init_browser()

    # Visit the url
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    # mars_weather
    mars_weather=soup.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)


    # In[68]:


    # * Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas
    # to scrape the table containing facts about the planet including Diameter, Mass, etc.
    #Use Pandas to convert the data to a HTML table string.
    # Initialize browser
    browser = init_browser()

    # Visit the url
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    facts = soup.find('table', class_='tablepress tablepress-id-mars')
    #print(facts)
    table=(pd.read_html(soup.find("table", class_="tablepress tablepress-id-mars").prettify(),skiprows=2))[0]
    table.rename(columns={0:"Description", 1:"Value"}, inplace=True)
    table_html = table.to_html(index=False)
    table_html = table_html.replace('\n', '')


    # In[69]:


    table_html


    # In[70]:


    table


    # In[71]:


    #Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)
    # to obtain high resolution images for each of Mar's hemispheres.
    #You will need to click each of the links to the hemispheres in order to find the 
    browser = init_browser()

    # Visit the url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # hemisphere_image_url_1
    base_url = "https://astrogeology.usgs.gov"

    links = [base_url + item.find(class_="description").a["href"] for item in soup.find_all("div",class_="item")]
    links


    # In[50]:


    #Save both the image url string for the full resolution hemisphere image, and the 
    # Hemisphere title containing the hemisphere name.hemisphere_image_urls = []
    #Use a Python dictionary to store the # data using the keys `img_url` and `title`.
    hemisphere_image_urls = []

    for url in links:
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        
        title = soup.find("div", class_="content").find("h2", class_="title").text.replace(" Enhanced","")
        img_url = base_url + soup.find("img", class_="wide-image")['src']
        hemisphere_image_urls.append({"title":title,"img_url":img_url})
        


    # In[ ]:


    browser.quit()


    # In[51]:


    hemisphere_image_urls


    # In[53]:


    #Append the dictionary with the image url string and the hemisphere title to a list. 
    # This list will contain one dictionary for each hemisphere.

    mars = {
            "news_title":news_title,
            "news_p":news_p,
            "featured_image_url":featured_image_url,
            "mars_weather":mars_weather,
            "table_html":table_html,
            "hemisphere_image_urls":hemisphere_image_urls
        }

    return mars

# In[54]:

# In[ ]:




