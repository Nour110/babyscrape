#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy
from scrapy.http import Request

class ImdbSpider(scrapy.Spider):
	name = 'imdb_spider'
    
    # We will restrict our spider to IMDB only
	allowed_domains = [
		"imdb.com"
	]
	
	start_urls = ['https://www.imdb.com/title/tt0098800/']
	
	
	def parse(self,response):
    		creds = response.css("[href^='fullcredits']").attrib["href"]
    		creds_url = response.url+creds
    		print(creds_url)
    		yield Request(creds_url, self.parse_full_credits)   		
    			
	def parse_full_credits(self,response):
		actors_list = response.css("table.cast_list td.primary_photo")
		actors_page = [actor.css("a").attrib["href"] for actor in actors_list]
		actors_urls = ["https://www.imdb.com"+end for end in actors_page]
		for url in actors_urls:
			yield Request(url, self.parse_actor_page)
		
	def parse_actor_page(self,response):
		human = response.css("h1.header span.itemprop::text").get()
		finder = response.css("div.filmo-row")
		work_list = [film.css("a::text").get() for film in finder]
		for pixels in work_list:
			yield {
				"actor": human,
				"media": pixels
			}