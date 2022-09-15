import pymongo

client = pymongo.MongoClient("mongodb+srv://root:mongodb123@cluster0.zlbwi.mongodb.net/?retryWrites=true&w=majority")
db = client.test
db1 = client['mongotest']
coll = db1['test']
coll1 = db1['thumbnails']