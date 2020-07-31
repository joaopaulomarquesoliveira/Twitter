from tweepy import Stream                   # tweepy import Stream and StreamListener because they are receive tweets in real time / Porque recebem tweets em tempo real
from tweepy import OAuthHandler             #for twitter authentication / para autenticação no twitter
from tweepy.streaming import StreamListener
from pymongo import MongoClient             #Connector Python/MongoDB
import pandas as pd
import json


#consumer key, consumer secret, access token, access secret.
#it's possible to get the keys, opening a developer account in https://developer.twitter.com/
#É possível obter as chaves, abrindo uma conta de desenvolvedor em https://developer.twitter.com/

ckey="7U1Mb2xh4JuZqFvLXxXQ0NpdK"
csecret="gY1UF2DnZoqYkFQEKVfVZerbNev4GTao08MI3d0UZw8RFVFOpl"
atoken="342377408-li0bFQ5dcIwrRfkUH4PSFvq0c7JhmHUoNkKIEypz"
asecret="9HxwWdbTGWXnsyDyITV5RaUAglACLIdfQtiujKHWiz2oI"

class listener(StreamListener):
    def on_data(self, status):
        twitter= json.loads(status)        
        created_at= twitter["created_at"]
        id_str= twitter["id_str"]
        text= twitter["text"]
        obj={"created_at": created_at,"id_str":id_str,"text":text}
        twitterid= col.insert_one(obj).inserted_id
        print (obj)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

conn=MongoClient('localhost',27017)
db=conn.twitterdb
col=db.tweets


twitterStream.filter(track=["python"])



twitterStream.disconnect()


dataset=[{'created_at': item["created_at"],'text': item["text"],} for item in col.find()]








df=pd.DataFrame(dataset)



from sklearn.feature_extraction.text import CountVectorizer



cv=CountVectorizer()



count_matrix=cv.fit_transform(df.text)



word_count=pd.DataFrame(cv.get_feature_names(), columns=['Palavras'])
word_count['count']=count_matrix.sum(axis=0).tolist()[0]
word_count=word_count.sort_values("count", ascending=False).reset_index(drop=True)
word_count[:50]








