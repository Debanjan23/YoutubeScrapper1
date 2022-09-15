import pymongo

client = pymongo.MongoClient("mongodb+srv://root:mongodb123@cluster0.zlbwi.mongodb.net/?retryWrites=true&w=majority")
db = client.test
db1 = client['Comment_data']
coll = db1['comments']
coll1 = db1['thumbnails']