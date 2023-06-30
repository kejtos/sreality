BOT_NAME = 'sreality_scraper'
SPIDER_MODULES = ['sreality_scraper.spiders']
NEWSPIDER_MODULE = 'sreality_scraper.spiders'
FEEDS = {'sreality.json': {'format': 'json', 'overwrite': True}}
ROBOTSTXT_OBEY = False
LOG_LEVEL = 'DEBUG'
ITEM_PIPELINES = {'sreality_scraper.pipelines.SrealityPipeline': 300,}
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEED_EXPORT_ENCODING = 'utf-8'

