"""
Example file to simulate an ETL process within a docker pipeline
- Extracts from a mongo db
- Transforms the collections
- Loads the transformed collections to postgres db

To be started by docker (see ../compose.yml)

For inspecting that ETL worked out: docker exec -it pipeline_example_my_postgres_1 psql
"""


import pymongo
import sqlalchemy
import psycopg2
import time
import logging
logging.basicConfig(level=logging.INFO)

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

s  = SentimentIntensityAnalyzer()


# mongo db definitions
try:
    client = pymongo.MongoClient('mongodb', port=27017)  # mongodb is the hostname (= service in yml file)
    db = client.reddit #change this to what your mongodb database is called
    coll = db.posts #change this to whatever your collection in that db is called
    logging.critical("\n---- successfully connected to mongoDB database ----\n")
except:
    logging.exception("Could not connect to mongoDB database")

# postgres db definitions. HEADS UP: outsource these credentials and don't push to github.
USERNAME_PG = 'postgres'
PASSWORD_PG = 'postgres'
HOST_PG = 'postgresdb'  # = name of the psql service in the yml file
PORT_PG = 5432
DATABASE_NAME_PG = 'reddits_pgdb' #Same as the POSTGRES_DB env variable in yml file

conn_string_pg = f"postgresql://{USERNAME_PG}:{PASSWORD_PG}@{HOST_PG}:{PORT_PG}/{DATABASE_NAME_PG}"
time.sleep(5)  # safety margin to ensure running postgres server
try:
    pg = sqlalchemy.create_engine(conn_string_pg).connect()
    logging.critical("\n---- successfully connected to postgres database ----\n")
except:
    logging.exception("Could not connect to postgres database")

# Create the table
create_table_string = sqlalchemy.text("""CREATE TABLE IF NOT EXISTS reddits (
					 id TEXT,
                                         title TEXT,
                                         sentiment NUMERIC
                                         );

                                      """)
try:
    pg.execute(create_table_string)
    pg.commit()
    logging.critical("\n---- successfully created table in postgres ----\n")
except:
    logging.exception("\n---- could not create table in postgres ----\n")

def extract():
    # We are loading only the last 5 entries for speed/debugging - you can do them all or change this as you need
    extracted_reddits = list(coll.find())
    logging.info(f"\n----reddits extracted from MongoDB----\n")
    return extracted_reddits
    
def regex_clean(reddit):
    #placeholder function for removing things from your reddit text, e.g. links.
    cleaned_text = reddit.replace("'", "")
    return cleaned_text

def sentiment_analysis(text):	
    #placeholder for real sentiment analysis function
    sentiment = s.polarity_scores(text)
    print(sentiment)
    score = sentiment['compound']
    
    return score

def transform(extracted_reddits):
    transformed_reddits = []
    for item in extracted_reddits:
        post=item
        # optional just to see what is going on:
        logging.info(f"Post currently being transformed:\n{post}")

        #here we select the 'text' key from the dictoinary
        text = post['text']

        #... clean it using the regex cleaning function (which currently does nothing)
        text = regex_clean(text)
        logging.info(f"Regex cleaning successful")
        #...perform sentiment analysis (currently returns 1 for all text - yours will be different)
        sentiment = sentiment_analysis(text)
        logging.info(f"Sentiment analysis performed")
        #... add a field to the post dictionary called "sentiment" that contains this value
        post['sentiment'] = sentiment

        # ... and finally append the post to our list of transformed reddits
        transformed_reddits.append(post)

        # can also optionally add a logging statement
        #(-think about if you want this inside or outside the for-loop)
        logging.info("\n---- new reddit post successfully transformed ----\n")
       
    return transformed_reddits


def load(transformed_reddits):
    for post in transformed_reddits:
        try:
            logging.info(f"Attempting to load transformed reddit post into postgres")
            insert_query = sqlalchemy.text("INSERT INTO reddits (id, title, sentiment) VALUES (:id, :title, :sentiment)")
            pg.execute(insert_query, {"id": post['_id'], "title": post['text'], "sentiment": post['sentiment']})
            pg.commit()
            logging.info(f"\n---- New reddit post incoming with sentiment score {post['sentiment']}:----\n {post['text']} ")
            logging.info("\n---- new reddit post loaded to postgres db ----\n")
        except:
            logging.exception("Something went wrong while inserting into psql")
    return None

if __name__ == '__main__':
    while True:
        extracted_reddits = extract()
        transformed_reddits = transform(extracted_reddits)
        load(transformed_reddits)
        time.sleep(10)
