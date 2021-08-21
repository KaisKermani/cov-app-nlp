from chalice import Chalice
import logging

from chalicelib.CovApi import CovApi
from chalicelib.FacebookScraper import FacebookScraper
from chalicelib.ScrapingHandler import ScrapingHandler

app = Chalice(app_name='scraper')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.schedule("5 minutes")
def scrape_facebook_groups(event):
    logger.info("Running scrape facebook groups scheduled job")
    email = "mahdouikenza@gmail.com"
    password = "nlp_kenza_Angle_123"
    geckodriver_path = "/opt/geckodriver"
    fb_scraper = FacebookScraper(email=email, password=password, geckodriver_path=geckodriver_path)
    cov_api = CovApi()
    handler = ScrapingHandler(fb_scraper=fb_scraper,api_service=cov_api)
    return handler.scrape()
