import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CovApi:
    def get_facebook_groups(self):
        return ["1493465070746580"]

    def insert_posts(self, posts, fb_group):

        # Inserting new posts in database:
        for row in posts:
            logger.info((
                row['id'], row['text'], row['Author'], row['Author_profile'], row['Post_time'], row['Extract_time'],
                row['Post_link'], fb_group))
