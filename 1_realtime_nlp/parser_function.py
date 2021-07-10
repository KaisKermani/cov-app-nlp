from queue import Queue
import operator
import spacy
import mysql.connector
from post_processor import post_process


def parser(input_q: Queue):

	nlp = spacy.load('../nlpModel')

	mydb = mysql.connector.connect(
		host="localhost",
		user="parser_nlp",
		password="nlp_cov_Parser_123",
		database='db_cov',
	)
	mycursor = mydb.cursor()

	print("Parser ready!")
	while True:
		post_id = input_q.get()

		mycursor.execute('SELECT * FROM raw where id="' + post_id + '"')
		try:
			raw = mycursor.fetchall()[0][1]
		except IndexError:
			continue

		doc = nlp(raw)

		entities = {'from': "", 'to': "", 'n_places': "", 'day': "", 'time': "", 'num': "", 'price': ""}
		for ent in doc.ents:
			try:
				entities[ent.label_] = entities[ent.label_] + str(ent) + ', '
			except IndexError:
				continue
		category = max(doc.cats.items(), key=operator.itemgetter(1))[0]

		entities = post_process(entities)
		
		values = str((
			post_id, entities['from'][:-2], entities['to'][:-2], entities['n_places'][:-2], entities['day'][:-2],
			entities['time'][:-2], entities['num'][:-2], entities['price'][:-2], category
		))
		try:
			mycursor.execute('insert into structured values ' + values)
			mydb.commit()
		except mysql.connector.errors.IntegrityError:
			pass
