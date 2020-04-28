#Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time
from urllib.parse import urlparse
import pymongo


def wait_to_load(browser):
    time_start = time.time()
    time.sleep(3)
    while browser.execute_script('return document.readyState;') != "complete":
        time.sleep(1)
    time_stop = time.time()
    return time_stop-time_start    



class Scrape_Mars_data():
    #Pages to be scraped  
    article_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    mars_images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    mars_facts_url = "https://space-facts.com/mars/"
    hemispheres_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    def __init__(self):
        #self.executable_path = {'executable_path': 'chromedriver.exe'}
        self.browser = Browser('chrome', headless=False)

    def get_latest_article(self, article_url=article_url):
        self.browser.visit(article_url)
        wait_to_load(self.browser)
        article_soup = bs(self.browser.html, 'html.parser')
        #get all list tags
        article_list_tags = article_soup.find_all('li', class_="slide")
        #determine the latest date
        article_dates=[]
        for article_list_tag in article_list_tags:
            article_dates = article_dates + [article_list_tag.find('div', class_="list_date").text]
        article_latest_date = max(pd.to_datetime(article_dates))
        #Determine the latest news title with corresponding paragraph
        for article_list_tag in article_list_tags:
            if pd.to_datetime( article_list_tag.find('div', class_="list_date").text ) == article_latest_date:
                news_title = article_list_tag.find('div', class_="content_title").text
                news_p = article_list_tag.find('div', class_="article_teaser_body").text
        return {"news_title": news_title, "teaser": news_p}
    
    def get_featured_image(self,mars_images_url=mars_images_url):
        self.browser.visit(mars_images_url)
        wait_to_load(self.browser)
        picture_soup = bs(self.browser.html, 'html.parser')
        #get all list tags
        picture_list_tags = picture_soup.find_all('li', class_="slide")
        #Determine the picture latest date
        try:
            picture_dates=[]
            for picture_list_tag in picture_list_tags:
                picture_dates = picture_dates + [picture_list_tag.find('h3', class_="release_date").text]
        except:
            pass
        picture_latest_date = max(pd.to_datetime(picture_dates))
        try:
            for picture_list_tag in picture_list_tags:
                if pd.to_datetime(picture_list_tag.find('h3', class_="release_date").text) == picture_latest_date:
                    # get picture relative link
                    picture_relative_link = picture_list_tag.a["data-fancybox-href"]
                    #get picture base link
                    link_elements = urlparse(mars_images_url)
                    picture_base_link=f"{link_elements.scheme}://{link_elements.netloc}"
                    #set picture full link
                    picture_full_link = picture_base_link+picture_relative_link
                    break
        except:
            pass
        return {"featured_picture_url" : picture_full_link}

    def get_mars_weather(self, mars_weather_url=mars_weather_url):
        self.browser.visit(mars_weather_url)
        wait_to_load(self.browser)
        #get the html of the weather
        weather_soup = bs(self.browser.html, 'html.parser')
        #Determine structure of the tweet list
        tweet_container_tags = weather_soup.find_all('div', class_="css-1dbjc4n r-my5ep6 r-qklmqi r-1adg3ll")
        #find te latest tweet date and get mars weather info
        tweet_dates = []
        mars_weather_info = []
        # try:
        for tweet_container_tag in tweet_container_tags:
            tweet_date = tweet_container_tag.find('a', class_="css-4rbku5 css-18t94o4 css-901oao r-1re7ezh r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0")
            tweet_date = pd.to_datetime(tweet_date["title"].replace(" · "," "))
            tweet_dates = tweet_dates + [tweet_date]
            latest_tweet_date = max(tweet_dates)
            #get Mars weather info
            if tweet_date == latest_tweet_date:
                mars_weather_info = tweet_container_tag.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
                mars_weather_info = mars_weather_info.span.text
        return {"mars_weather_url" : mars_weather_info}

    def get_mars_facts(self, mars_facts_url=mars_facts_url):
        self.browser.visit(mars_facts_url)
        wait_to_load(self.browser)
        tables = pd.read_html(self.browser.html)
        mars_facts_table = tables[0].rename(columns={0:"Description",1:"Value"}).set_index("Description")
        return {"mars_facts_table": mars_facts_table.to_html()}

    def get_hemisphere_pictures(self, hemispheres_url=hemispheres_url):
        #get hemisphere image names
        self.browser.visit(hemispheres_url)
        hemisphere_soup = bs(self.browser.html, 'html.parser')
        hemisphere_titles = hemisphere_soup.find_all('h3')
        hemisphere_image_names = [hemisphere_title.text for hemisphere_title in hemisphere_titles]
        # get links for the emisphere pictures
        hemisphere_image_links = []
        for title in hemisphere_image_names:
            #click on each link
            self.browser.click_link_by_partial_text(title)
            wait_to_load(self.browser)
            hemisphere_soup = bs(self.browser.html, 'html.parser')
            link_elements = urlparse(self.browser.url)
            image_base_link=f"{link_elements.scheme}://{link_elements.netloc}"
            relative_image_link = hemisphere_soup.find('img',class_="wide-image")["src"]
            image_link=image_base_link+relative_image_link
            hemisphere_image_links.append(image_link)
            self.browser.visit(hemispheres_url)
            wait_to_load(self.browser)

        return {"titles": hemisphere_image_names, "links": hemisphere_image_links}

def scrape_and_store(connection_string='mongodb://localhost:27017'):
    #connect to database
    client = pymongo.MongoClient(connection_string)
    db = client.mars_db
    #remove any part recordings
    db.mars.drop()
    #select collection to store recordings
    collection = db.mars
    scrape = Scrape_Mars_data()
    #Store article data
    scrape_id = collection.insert_one(scrape.get_latest_article()).inserted_id
    #store picture url
    collection.update_one({"_id":scrape_id}, {'$set':scrape.get_featured_image()})
    #store mars weather
    collection.update_one({"_id":scrape_id}, {'$set':scrape.get_mars_weather()})
    #store mars facts
    collection.update_one({"_id":scrape_id}, {'$set':scrape.get_mars_facts()})
    #store hemisphere pictures url
    collection.update_one({"_id":scrape_id}, {'$set':scrape.get_hemisphere_pictures()})


        



#for testing only
if __name__ == "__main__":
#    scrape_instance = Scrape_Mars_data()
#    print(scrape_instance.get_latest_article())
#    print(scrape_instance.get_featured_image())
#    print(scrape_instance.get_mars_weather())
#    print(scrape_instance.get_mars_facts())
#    scrape_instance = Scrape_Mars_data()
#    print(scrape_instance.get_hemisphere_pictures())
    scrape_and_store()

    

        