from Schema import  mongo_client as mc
import Data as d
import requests
import pandas as ps
import base64

d1=d.Data()

class Load_Data:
           def load_mongo(data):
               try:
                   df = ps.DataFrame(data)
                   i=0
                   while i < 50 :
                       d = d1.get_comments_by_id(df['video_id'][i])
                       mn = dict(data=d, name=df['Youtuber_name'][i])
                       mc.coll.insert_one(mn)
                       i = i + 1

                   j = 0
                   while j < 50 :
                       mn1 = dict(d_thumnail_base64=get_as_base64(df['Thumbnail'][j]), video_id=df['video_id'][j])
                       mc.coll1.insert_one(mn1)
                       j = j + 1

                   return 1

               except Exception as e:
                   print(e)

def get_as_base64(url) :

       return base64.b64encode(requests.get(url).content)
