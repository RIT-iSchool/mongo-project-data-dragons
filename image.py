from pymongo import MongoClient
import gridfs
from pprint import pprint
import os

db = MongoClient('mongodb://root:student@localhost:27017').get_database('Flickr')
fs = gridfs.GridFS(db)

img_path = os.getcwd() + "/github-classroom/RIT-iSchool/mongo-project-data-dragons/images/"
img_names = [f for f in os.listdir(img_path)]

# count = 0
# for img_name in img_names:
#     img_new_path = img_path + "/" + img_name
#     with open (img_new_path,"rb") as img:
#         imgMeta = {
#             "photo_id": img_name.split('.')[0]
#         }
#         uid = fs.put(img, fileName=img_name, metadata=imgMeta)
#         print(uid)
#         count +=1
# print(count)

fsFilesColl = db["fs.files"]
fsChunksColl = db["fs.chunks"]

cursor = fsFilesColl.find({
    'metadata': {'photo_id': '40429722313'}
})

for item in cursor:
    pprint(item)
