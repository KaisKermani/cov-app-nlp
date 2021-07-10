import random

import mysql.connector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import hashlib
import time
from datetime import datetime, timedelta
from fb_coordinates import email, passwd

import threading
from queue import Queue
import sys
sys.path.insert(1, '../1_realtime_nlp')
from parser_function import parser


def format_post_id(link):
	return link.split('permalink/')[1].split('/')[0]


def format_profile_id(link):
	return link.split("facebook.com/")[1].split('groupid')[0].split('profile.php?id=')[-1].split('?')[0].split('&')[0]


def format_extract_time(ts):
	return datetime.strptime(ts, '%a %b %d %H:%M:%S %Y').strftime("%Y-%m-%d %H:%M:%S")


def format_post_time(ts, extract_time):
	try:
		formatted = datetime.strptime(ts, '%d %B at %H:%M')
		extract = datetime.strptime(extract_time, '%Y-%m-%d %H:%M:%S')
		formatted = formatted.replace(year=extract.year)
		return formatted.strftime("%Y-%m-%d %H:%M:%S")
	except ValueError:
		try:
			formatted = datetime.strptime(ts, '%d %B %Y at %H:%M').strftime("%Y-%m-%d %H:%M:%S")
			return formatted
		except ValueError:
			pass
	extract = datetime.strptime(extract_time, '%Y-%m-%d %H:%M:%S')
	if ts == 'Just now':
		return extract_time
	else:
		try:
			elts = ts.split(' ')
			if 'min' in elts or 'mins' in elts:
				return (extract - timedelta(minutes=int(elts[0]))).strftime("%Y-%m-%d %H:%M:%S")
			
			elif 'hr' in elts or 'hrs' in elts:
				return (extract - timedelta(hours=int(elts[0]), minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
			
			elif 'Yesterday' in elts:
				day = extract - timedelta(days=1)
				formatted = datetime.strptime(ts, 'Yesterday at %H:%M')
				formatted = formatted.replace(day=day.day, month=day.month, year=day.year)
				return formatted.strftime("%Y-%m-%d %H:%M:%S")
		except:
			return extract_time

		
def find_last_article():
	ind = 1
	while True:
		try:
			browser.find_element_by_xpath(
				'/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * (ind - 1) + '/section/article[20]'
			)
			ind = ind + 1
		except NoSuchElementException:
			return (ind - 1) * 20


def scroll_till(n):
	last = find_last_article()
	while last < n:
		browser.find_element_by_tag_name("body").send_keys(Keys.END)
		try:
			WebDriverWait(browser, 5).until(ec.presence_of_element_located((
				By.XPATH, '/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int(last / 20) +
				'/section/article[1]')
			))
		except TimeoutException:
			print('couldn\'t load more posts!')
		last = find_last_article()


# Parser thread
output_q = Queue()
parser_thread = threading.Thread(
	target=parser,
	args=[output_q],
	name='parser'
)
parser_thread.start()

# Connection to the database
mydb = mysql.connector.connect(
	host="localhost",
	user="scraper_nlp",
	password="nlp_cov_Scraper_123",
	database='db_cov',
)
mycursor = mydb.cursor()

# Connection to facebook
browser = webdriver.Firefox()
browser.get("https://mobile.facebook.com/groups/1493465070746580")
browser.find_element_by_xpath("//input[@id='m_login_email']").send_keys(email)
browser.find_element_by_xpath("//input[@id='m_login_password']").send_keys(passwd)
browser.find_element_by_xpath("//input[@id='m_login_password']").send_keys(Keys.ENTER)

WebDriverWait(browser, 10).until(ec.presence_of_element_located(
	(By.XPATH, '/html/body/div[1]/div/div[4]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div')
))


mycursor.execute("SELECT * FROM fb_groups")
fb_groups = mycursor.fetchall()
# fb_groups = [('0', '1344373312324134', '1344373312324134', '3')]
last_posts = {}
for group in fb_groups:
	last_posts[group[2]] = ""

max_posts_per_group = 20
sleep_duration = 40

while True:
	for group_info in fb_groups:
		group = group_info[2]
		posts = []
		post = {}

		browser.get("https://mobile.facebook.com/groups/" + group)
		WebDriverWait(browser, 5).until(ec.presence_of_element_located(
			(By.XPATH, '/html/body/div[1]/div/div[4]/div/div[1]/div/div/section/article[1]')
		))

		for i in range(1, max_posts_per_group + 1):

			if (i-1) % 20 == 0:
				scroll_till(i)
			
			try:
				post['text'] = browser.find_element_by_xpath(
					'/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int((i - 1) / 20) +
					'/section/article[' + str((i - 1) % 20 + 1) + ']/div/div/div/span/p'
				).text

			except NoSuchElementException:
				try:
					post['text'] = browser.find_element_by_xpath(
						'/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int((i - 1) / 20) +
						'/section/article[' + str((i - 1) % 20 + 1) + ']/div/div/div/div/span[2]/span/span'
					).text

				except NoSuchElementException:
					try:
						post['text'] = browser.find_element_by_xpath(
							'/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int((i - 1) / 20) +
							'/section/article[' + str((i - 1) % 20 + 1) + ']/div/div[2]/div[1]/div[4]/div/span'
						).text
					
					except NoSuchElementException:
						try:
							post['text'] = browser.find_element_by_xpath(
								'/html/body/div[1]/div/div[4]/div/div[1]/div/div[4]' + '/div' * int((i - 1) / 20) +
								'/section/article[' + str((i - 1) % 20 + 1) + ']/div/div/div/span'
							).text
						
						except NoSuchElementException:
							print('POST #' + str(i) + ' NOT VALID')
							continue

			try:
				post['Post_time'] = browser.find_element_by_xpath(
					'/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int((i - 1) / 20) +
					'/section/article[' + str(
						(i - 1) % 20 + 1) + ']/div/header/div/div[2]/div/div/div/div[1]/div/a/abbr'
				).text
				post['Extract_time'] = time.ctime(time.time())
				try:
					post['Author'] = browser.find_element_by_xpath(
						'/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int((i - 1) / 20) +
						'/section/article[' + str(
							(i - 1) % 20 + 1) + ']/div/header/div/div[2]/div/div/div/div[1]/h3/span/strong[1]/a'
					).text
					post['Author_profile'] = browser.find_element_by_xpath(
						'/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int((i - 1) / 20) +
						'/section/article[' + str(
							(i - 1) % 20 + 1) + ']/div/header/div/div[2]/div/div/div/div[1]/h3/span/strong[1]/a'
					).get_attribute('href')
				except NoSuchElementException:
					post['Author'] = browser.find_element_by_xpath(
						'/html/body/div[1]/div/div[4]/div/div[1]/div/div[4]' + '/div' * int((i - 1) / 20) +
						'/section/article[' + str(
							(i - 1) % 20 + 1) + ']/div/header/div/div[2]/div/div/div/div[1]/h3/strong/a'
					).text
					post['Author_profile'] = browser.find_element_by_xpath(
						'/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int((i - 1) / 20) +
						'/section/article[' + str(
							(i - 1) % 20 + 1) + ']/div/header/div/div[2]/div/div/div/div[1]/h3/strong/a'
					).get_attribute('href')
		
				try:
					post['Post_link'] = browser.find_element_by_xpath(
						'/html/body/div[1]/div/div[4]/div/div[1]/div/div' + '/div' * int((i - 1) / 20) +
						'/section/article[' + str(
							(i - 1) % 20 + 1) + ']/div/div/a'
					).get_attribute('href')
				except NoSuchElementException:
					post['Post_link'] = browser.find_element_by_xpath(
						'/html/body/div[1]/div/div[4]/div/div[1]/div/div[4]' + '/div' * int((i - 1) / 20) +
						'/section/article[' + str(
							(i - 1) % 20 + 1) + ']/div/header/div/div[2]/div/div/div/div[1]/div/a'
					).get_attribute('href')
					'/html/body/div[1]/div/div[4]/div/div/div[4]/section/article[3]/div/header/div/div[2]/div/div/div/div[1]/div/a'

			except NoSuchElementException:
				print('POST #' + str(i) + ' PROBLEMATIC')
				continue

			post['Post_link'] = format_post_id(post['Post_link'])
			post['Author_profile'] = format_profile_id(post['Author_profile'])
			post['id'] = hashlib.md5((post['text'] + post['Post_link']).encode()).hexdigest()
			post['Extract_time'] = format_extract_time(post['Extract_time'])
			post['Post_time'] = format_post_time(post['Post_time'], post['Extract_time'])
			if post['id'] == last_posts[group]:
				break

			posts.append(dict(post))

		try:
			last_posts[group] = posts[0]['id']
			print(group, 'extracted:', len(posts))
		except IndexError:
			continue

		# Inserting new posts in database:
		for row in posts:
			sql_values = str((
				row['id'], row['text'], row['Author'], row['Author_profile'], row['Post_time'], row['Extract_time'],
				row['Post_link'], group)
			)
			try:
				mycursor.execute('insert into raw values ' + sql_values)
				mydb.commit()
			except mysql.connector.errors.IntegrityError:
				continue

			output_q.put(row['id'])

		time.sleep(random.random()*10+3)

	time.sleep(random.random()*sleep_duration + sleep_duration)
