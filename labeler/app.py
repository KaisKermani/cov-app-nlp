import operator

import logging
import os
import spacy
import itertools

from chalicelib.CovApi import CovApi

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_STREAM_ARN = os.environ.get('TABLE_STREAM_ARN')
COV_API_URL = os.environ.get('COV_API_URL')

logger.info("Loading nlp model")
nlp = spacy.load("/opt/nlpModel")


def on_table_update(event, context):
    logger.info(f"Received event {event}")
    cov_api = CovApi(COV_API_URL)
    for record in event["Records"]:
        if record.get("eventName") != 'INSERT':
            return
        new_item = record.get('dynamodb').get('NewImage')
        if new_item["SK"]["S"] != "raw":
            return
        row = process_new_image(new_item)
        cov_api.insert_structured(row)


def process_new_image(new_item):
    raw_text = new_item["post_text"]["S"]
    doc = nlp(raw_text)

    # Group by entities and convert
    entities = {key: ",".join(str(e) for e in g) for key, g in itertools.groupby(sorted(doc.ents, key=lambda x: x.label_), lambda x: x.label_)}
    category = max(doc.cats.items(), key=operator.itemgetter(1))[0]
    name_map = {
        "day": "cov_day",
        "time": "cov_time",
        "from": "loc_from",
        "to": "loc_to",
        "n_places": "n_seats",
        "num": "phone",
        "price": "cost"
    }
    res = {name_map[name]: val for name, val in entities.items()}
    res["category"] = category
    res["id"] = new_item["id"]["S"]
    print(res)
    return res
