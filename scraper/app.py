from chalice import Chalice
import logging

from chalicelib.ScrapingHandler import ScrapingHandler

app = Chalice(app_name='scraper')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.schedule("5 minutes")
def scrape_facebook_groups(event, context):
    logger.info("Running scrape facebook groups scheduled job")
    handler = ScrapingHandler()
    return handler.scrape()
