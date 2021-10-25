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
	
	# This is our chosen favorite TV show or movie's IMDB page which we will be scraping
	start_urls = ['https://www.imdb.com/title/tt0098800/']
	
	
	def parse(self,response):
	"""
	This function, which assumes that we are on the IMDB page of a movie or tv show\
	will extract a link to the cast and crew list which is also located on IMDB.\
	Once we have that link we will call the parse_full_credits method on the cast and crew page.
	"""
		# This will extract the path to the full credits page on IMDB for our favorite show
    		creds = response.css("[href^='fullcredits']").attrib["href"]
    		
    		# Append the path to the URL of our favorite show to access its full credits page
    		creds_url = response.url+creds
    		
    		# Call parse_full_credits on the URL of the full credits page
    		yield Request(creds_url, self.parse_full_credits)   		
    			
	def parse_full_credits(self,response):
	"""
	This function, which assumes we are on a cast and crew page of a show on IMDB\
	will create a list of URLs to each cast member's IMDB page (only the actors)\
	For each actor, we call the parse_actor_page method on their IMDB page
	"""
		# Here we extract the path to each of the actor's IMDB page
		actors_list = response.css("table.cast_list td.primary_photo")
		actors_page = [actor.css("a").attrib["href"] for actor in actors_list]
		
		# Append the path of the actor's IMDB page to the IMDB domain
		actors_urls = ["https://www.imdb.com"+end for end in actors_page]
		
		# for each actor, we call parse_actor_page for their page.
		for url in actors_urls:
			yield Request(url, self.parse_actor_page)
		
	def parse_actor_page(self,response):
	"""
	This function assumes we are on an actor's IMDB page.
	It will extract the name of the actor from the page and the name of every\
	show in their filmography.\
	Then it will save this to a csv file with two columns:\
		1. The name of the actor
		2. The name of the show that the actor worked on
	"""
		# We extract the name of the actor	
		human = response.css("h1.header span.itemprop::text").get()
		
		# Extract the name of every show in the actor's filmography
		finder = response.css("div.filmo-row")
		work_list = [film.css("a::text").get() for film in finder]
		
		# Output to a csv as described
		for pixels in work_list:
			yield {
				"actor": human,
				"media": pixels
			}