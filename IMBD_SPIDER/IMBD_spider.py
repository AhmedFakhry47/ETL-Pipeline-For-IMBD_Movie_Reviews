from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from pymongo import MongoClient
import pymongo
import scrapy


def connect_database():
	cluster = MongoClient("mongodb+srv://enihcam:12345@cluster0.irbss.mongodb.net/<Movie_Review>?retryWrites=true&w=majority")
	db = cluster["Movie_Review"]
	collection = db["IMBD_Reviews"]
	return collection


SEARCH_QUERY=(
	'https://www.imdb.com/search/title?'
    'title_type=feature&'
    'user_rating=1.0,10.0&'
    'countries=us&'
    'languages=en&'
    'count=250&'
    'view=simple'
    )

class IMBD_spider(scrapy.spiders.Spider):
	name = 'IMBD_spider'
	allowed_domains = ['imdb.com']
	start_urls = [SEARCH_QUERY]

	rules = (Rule(
        LinkExtractor(restrict_css=('div.desc a')),
        follow=True,
        callback='parse',
    ),)

	database = connect_database()

	def parse(self,response):
		links = response.css('span.lister-item-header a::attr(href)').extract()		
		#print('here',links)
		for link in links:
			yield response.follow(link,callback=self.parse_movie)


	def parse_movie(self,response):
		data = {}
		data['title'] = response.css('h1::text').extract_first().strip()

		#data['rating'] = response.css('.subtext::text').extract_first().strip() or None
		data['year'] = response.css('#titleYear a::text').extract_first()
		data['users_rating'] = response.xpath('//span[contains(@itemprop, "ratingValue")]/text()').extract_first()
		data['votes'] = response.xpath('//span[contains(@itemprop, "ratingCount")]/text()').extract_first()
		data['datascore'] = response.xpath('//div[contains(@class, "datacriticScore")]/span/text()').extract_first()
		data['img_url'] = response.xpath('//div[contains(@class, "poster")]/a/img/@src').extract_first()
		countries = response.xpath('//div[contains(@class, "txt-block") and contains(.//h4, "Country")]/a/text()').extract()
		data['countries'] = [country.strip() for country in countries]
		languages = response.xpath('//div[contains(@class, "txt-block") and contains(.//h4, "Language")]/a/text()').extract()
		data['languages'] = [language.strip() for language in languages]
		actors = response.xpath('//td[not(@class)]/a/text()').extract()
		data['actors'] = [actor.strip() for actor in actors]
		genres = response.xpath("//div[contains(.//h4, 'Genres')]/a/text()").extract()
		data['genre'] = [genre.strip() for genre in genres]
		tagline = response.xpath('//div[contains(string(), "Tagline")]/text()').extract()
		data['tagline'] = ''.join(tagline).strip() or None
		data['description'] = response.xpath('//div[contains(@class, "summary_text")]/text()').extract_first().strip() or None
		directors = response.xpath("//div[contains(@class, 'credit_summary_item') and contains(.//h4, 'Director')]/a/text()").extract() or None
		if directors: data['directors'] = [director.strip() for director in directors]
		data['runtime'] = response.xpath("//div[contains(@class, 'txt-block') and contains(.//h4, 'Runtime')]/time/text()").extract_first() or None
		data['imdb_url'] = response.url.replace('?ref_=adv_li_tt', '')

		reviews_link = response.xpath("//div[contains(@class,'subnav')]/div[@id='quicklinksMainSection']/a[@class='quicklink'][3]/@href").extract()
		yield response.follow(reviews_link[0],meta={'movie_info':data},callback=self.parse_reviews)


	def parse_reviews(self,response):
		data = response.meta['movie_info'] 
		reviews = response.xpath("//div[@class='text show-more__control']/text()").extract()
		stars   = response.xpath("//span[@class='rating-other-user-rating']/span/text()").extract()[::2]

		#Storing data in database
		current_movie = {x:data[x] for x in data.keys()}
		current_movie['_id']= current_movie['title']
		current_movie['Reviews'] = {str(j):[i,v] for j,i,v in zip(list(range(0,len(stars))),reviews,stars)}
		del(current_movie['title']) 
		self.database.insert_one(current_movie)


		yield None





