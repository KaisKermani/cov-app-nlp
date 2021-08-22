import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CovApi:

    def insert_structured(self, structured):
        # Inserting new structured entry in db
        logger.info(f"Inserting {structured} to db")