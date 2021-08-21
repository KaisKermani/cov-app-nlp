class CovApi:
    def get_facebook_groups(self):
        mycursor.execute("SELECT * FROM fb_groups")
        fb_groups = mycursor.fetchall()
        # fb_groups = [('0', '1344373312324134', '1344373312324134', '3')]
        last_posts = {}
        for group in fb_groups:
            last_posts[group[2]] = ""

    def insert_posts(self, posts):

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

        time.sleep(random.random() * 10 + 3)
