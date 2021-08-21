from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import hashlib
import time

import logging

from chalicelib.utils import fb_formatter

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ScrapingError(Exception):
    pass


class FacebookScraper:
    max_posts_per_group = 20

    def __init__(self, email: str, password: str, geckodriver_path: str):
        self.browser = webdriver.Firefox(
            executable_path=geckodriver_path
        )
        self.email = email
        self.password = password

    def connect_to_facebook(self):
        self.browser.get("https://mobile.facebook.com/groups/1493465070746580")
        self.browser.find_element_by_xpath("//input[@id='m_login_email']").send_keys(self.email)
        self.browser.find_element_by_xpath("//input[@id='m_login_password']").send_keys(self.password)
        self.browser.find_element_by_xpath("//input[@id='m_login_password']").send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 10).until(ec.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div[4]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div')
        ))

    def find_last_article(self):
        ind = 1
        while True:
            try:
                self.browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * (ind - 1) + '/section/article[20]'
                )
                ind += 1
            except NoSuchElementException:
                return (ind - 1) * 20

    def scroll_till(self, n):
        last = self.find_last_article()
        while last < n:
            self.browser.find_element_by_tag_name("body").send_keys(Keys.END)
            try:
                WebDriverWait(self.browser, 5).until(ec.presence_of_element_located((
                    By.XPATH, '/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int(last / 20) +
                    '/section/article[1]')
                ))
            except TimeoutException:
                logger.info("Couldn't load more posts!")
            last = self.find_last_article()

    def scrape_group(self, group_info):
        posts = []
        post = {}

        self.browser.get("https://mobile.facebook.com/groups/" + group_info)
        WebDriverWait(self.browser, 10).until(ec.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div[4]/div/div[1]/div/div/section/article[1]')
        ))

        for i in range(1, self.max_posts_per_group + 1):

            if (i - 1) % 20 == 0:
                self.scroll_till(i)


            try:
                post["text"] = self.find_post_text(i)
                post['Post_time'] = self.find_post_time(i)
                post['Extract_time'] = time.ctime(time.time())

                post['Author'], post['Author_profile'] = self.find_author_data(i)

                post['Post_link'] = self.find_post_link(i)

            except ScrapingError:
                logger.error('POST #' + str(i) + ' PROBLEMATIC')
                continue

            post['Post_link'] = fb_formatter.format_post_id(post['Post_link'])
            post['Author_profile'] = fb_formatter.format_profile_id(post['Author_profile'])
            post['id'] = hashlib.md5((post['text'] + post['Post_link']).encode()).hexdigest()
            post['Extract_time'] = fb_formatter.format_extract_time(post['Extract_time'])
            post['Post_time'] = fb_formatter.format_post_time(post['Post_time'], post['Extract_time'])
            logger.info("Check if post is already scraped")

            posts.append(dict(post))

        try:
            logger.info("Update last group")
        except IndexError:
            return

        return posts

    def find_post_text(self, i: int):
        try:
            return self.browser.find_element_by_xpath(
                '/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int((i - 1) / 20) +
                '/section/article[' + str((i - 1) % 20 + 1) + ']/div/div/div/span/p'
            ).text

        except NoSuchElementException:
            try:
                return self.browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int((i - 1) / 20) +
                    '/section/article[' + str((i - 1) % 20 + 1) + ']/div/div/div/div/span[2]/span/span'
                ).text

            except NoSuchElementException:
                try:
                    return self.browser.find_element_by_xpath(
                        '/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int((i - 1) / 20) +
                        '/section/article[' + str((i - 1) % 20 + 1) + ']/div/div[2]/div[1]/div[4]/div/span'
                    ).text

                except NoSuchElementException:
                    try:
                        return self.browser.find_element_by_xpath(
                            '/html/body/div[1]/div/div[4]/div/div[1]/div/div[4]' + '/div' * int((i - 1) / 20) +
                            '/section/article[' + str((i - 1) % 20 + 1) + ']/div/div/div/span'
                        ).text

                    except NoSuchElementException:
                        logger.info('POST #' + str(i) + ' NOT VALID')
                        raise ScrapingError(f"Post {i} NOT VALID")

    def find_post_link(self, i:int):

        try:
            return self.browser.find_element_by_xpath(
                '/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int((i - 1) / 20) +
                '/section/article[' + str(
                    (i - 1) % 20 + 1) + ']/div/div/a'
            ).get_attribute('href')
        except NoSuchElementException:
            pass
        try:
            return self.browser.find_element_by_xpath(
                '/html/body/div[1]/div/div[4]/div/div[1]/div/div[4]' + '/div' * int((i - 1) / 20) +
                '/section/article[' + str(
                    (i - 1) % 20 + 1) + ']/div/header/div/div[2]/div/div/div/div[1]/div/a'
            ).get_attribute('href')
            '/html/body/div[1]/div/div[4]/div/div/div[4]/section/article[3]/div/header/div/div[2]/div/div/div/div[1]/div/a'

        except NoSuchElementException:
            raise ScrapingError("Can't find post link")

    def find_author_data(self, i: int):

        try:
            el = self.browser.find_element_by_xpath(
                '/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int((i - 1) / 20) +
                '/section/article[' + str(
                    (i - 1) % 20 + 1) + ']/div/header/div/div[2]/div/div/div/div[1]/h3/span/strong[1]/a'
            )
            author = el.text
            author_profile = el.get_attribute('href')
            return author, author_profile
        except NoSuchElementException:
            pass

        try:
            el = self.browser.find_element_by_xpath(
                '/html/body/div[1]/div/div[4]/div/div[1]/div/div[4]' + '/div' * int((i - 1) / 20) +
                '/section/article[' + str(
                    (i - 1) % 20 + 1) + ']/div/header/div/div[2]/div/div/div/div[1]/h3/strong/a'
            )
            author = el.text
            author_profile = el.get_attribute('href')
            return author, author_profile
        except NoSuchElementException:
            logger.error("Could not find author data")
            raise ScrapingError("Couldn't find author data")

    def find_post_time(self, i:int):
        try:
            return self.browser.find_element_by_xpath(
            '/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int((i - 1) / 20) +
            '/section/article[' + str(
                (i - 1) % 20 + 1) + ']/div/header/div/div[2]/div/div/div/div[1]/div/a/abbr'
            ).text
        except NoSuchElementException:
            logger.error("Couldn't find post time")
            raise ScrapingError("Couldn't find post time")