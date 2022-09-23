import time
import pymongo
import psycopg2

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


s  = SentimentIntensityAnalyzer()



# Establish a connection to the MongoDB server
client = pymongo.MongoClient(host="mongodb", port=27017)

time.sleep(10)  # seconds

# Select the database you want to use withing the MongoDB server
db = client.twitter



  
from sqlalchemy import create_engine   
pg = create_engine('postgresql://postgres:1234@postgresdb:5432/tweets', echo=True) 

# pg = create_engine('postgresql://user:password@host:5432/dbname', echo=True)

pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(500),
    sentiment NUMERIC
);
''')


#docs = db.tweets.find(limit=10)

docs = db.tweets.find(limit=200)
  
for doc in docs:
    print(doc) 
    sentiment = s.polarity_scores(doc['text']) # assuming your JSON docs have a text field
    score = sentiment['compound']
    text = doc['text']
    query = "INSERT INTO tweets VALUES (%s, %s);"
  # replace placeholder from the ETL chapter
    pg.execute(query, (text, score))










