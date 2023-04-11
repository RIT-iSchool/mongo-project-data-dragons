import os
from pymongo import MongoClient


db = MongoClient('mongodb://dbadmin:student@localhost:27017').get_database('Flickr')
db.drop_collection('comment')
db.create_collection('comment')
comment = db.get_collection('comment')
collection = db['ImageDetails']
# img_path = os.getcwd() + "/github-classroom/RIT-iSchool/mongo-project-data-dragons/images/"
# img_names = [f for f in os.listdir(img_path)]


# count = 0
# for img_name in img_names:
#     uid = comment.insert_one({
#          "photo_id": img_name.split('.')[0],
#          "comments": ["Default First Comment"]
#     })
#     print(uid)
#     count +=1
# print(count)


cursor = collection.find({})

count = 0
for item in cursor:
    print(item)
    photo_ids = item['photo_id']
    comment.insert_one({
        "photo_id": str(photo_ids),
        "comments": []
    })
    count+=1
print(count)
