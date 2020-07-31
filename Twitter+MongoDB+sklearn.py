from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from pymongo import MongoClient
import json


#consumer key, consumer secret, access token, access secret.
ckey="7U1Mb2xh4JuZqFvLXxXQ0NpdK"
csecret="gY1UF2DnZoqYkFQEKVfVZerbNev4GTao08MI3d0UZw8RFVFOpl"
atoken="342377408-li0bFQ5dcIwrRfkUH4PSFvq0c7JhmHUoNkKIEypz"
asecret="9HxwWdbTGWXnsyDyITV5RaUAglACLIdfQtiujKHWiz2oI"

class listener(StreamListener):

    def on_data(self, status):
        a=json.loads(status)
        
        created_at = a["created_at"]
        id_str=a["id_str"]

        text= a["text"]
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




(col.find_one())




dataset=[{'created_at': item["created_at"],'text': item["text"],} for item in col.find()]




import pandas as pd




df=pd.DataFrame(dataset)



from sklearn.feature_extraction.text import CountVectorizer



cv=CountVectorizer()



count_matrix=cv.fit_transform(df.text)



word_count=pd.DataFrame(cv.get_feature_names(), columns=['Palavras'])
word_count['count']=count_matrix.sum(axis=0).tolist()[0]
word_count=word_count.sort_values("count", ascending=False).reset_index(drop=True)
word_count[:50]








