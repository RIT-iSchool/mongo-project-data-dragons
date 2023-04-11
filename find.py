import os
from pymongo import MongoClient


db = MongoClient('mongodb://root:student@localhost:27017').get_database('Flickr')
imaged = db.get_collection("ImageDetails")

img_path = os.getcwd() + "/github-classroom/RIT-iSchool/mongo-project-data-dragons/images/"
img_names = [f for f in os.listdir(img_path)]

count = 0
for img_name in img_names:
    cursor = imaged.find_one(
        {
            "photo_id": int(img_name.split('.')[0])
        },
        {
            'title':1
        }
    )
    print(cursor)
    count +=1
print(count)