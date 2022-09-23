import time
import requests
from sqlalchemy import create_engine   
import os
import psycopg2
import logging

webhook_url = "https://hooks.slack.com/services/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"


pg = create_engine('postgresql://postgres:1234@postgresdb:5432/tweets', echo=True)





tweets_result = pg.execute('''
    SELECT * FROM tweets LIMIT 200
;
''') 

for k in tweets_result:  
    k._asdict()
    data = {'text': k['text'] + "\n Tweet sentiment score is:" + " " + str(k['sentiment'])}
    print(data)
    #print(type(i))
    
       
# data = {'text': joke}

requests.post(url=webhook_url, json = data)

