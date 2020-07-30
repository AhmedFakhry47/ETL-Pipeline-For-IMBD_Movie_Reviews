from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(IMBD_spider)
process.start()