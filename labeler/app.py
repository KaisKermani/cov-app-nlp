import operator

from chalice import Chalice
import logging
import os
import spacy

app = Chalice(app_name='labeler')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_STREAM_ARN = os.environ['TABLE_STREAM_ARN']


@app.on_dynamodb_record(stream_arn=TABLE_STREAM_ARN)
def on_table_update(event):
    for record in event:
        process_record(record)


def process_record(record):
    # We're not interested in deleted items.
    if record.event_name == 'DELETE':
        return
    new_item = record.new_image

    raw_text = new_item["post_text"]["S"]
    nlp = spacy.load("./nlpModel")
    doc = nlp(raw_text)

    entities = {'from': "", 'to': "", 'n_places': "", 'day': "", 'time': "", 'num': "", 'price': ""}
    for ent in doc.ents:
        try:
            entities[ent.label_] = entities[ent.label_] + str(ent) + ', '
        except IndexError:
            continue
    category = max(doc.cats.items(), key=operator.itemgetter(1))[0]

