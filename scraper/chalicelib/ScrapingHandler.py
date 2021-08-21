import logging

from chalicelib.FacebookScraper import FacebookScraper

from chalicelib.CovApi import CovApi

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ScrapingHandler:
    def __init__(self, fb_scraper: FacebookScraper, api_service: CovApi):
        self.fb_scraper = fb_scraper
        self.api_service = api_service

    def scrape(self):
        self.fb_scraper.connect_to_facebook()

        # Get facebook groups
        fb_groups = self.api_service.get_facebook_groups()

        for group_info in fb_groups:
            self.fb_scraper.scrape_group(group_info)


