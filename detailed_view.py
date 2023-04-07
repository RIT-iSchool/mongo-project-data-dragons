import base64
import codecs
from bson import ObjectId
from pymongo import MongoClient
import gridfs

# Get database and collection
db = MongoClient('mongodb://root:student@localhost:27017').get_database('Flickr')
image_details  = db.get_collection('ImageDetails')
fs = gridfs.GridFS(db)
fsFilesColl = db["fs.files"]
fsChunksColl = db["fs.chunks"]

# Get the image details from the id
# def get_image_details(image_id):
#     photo_details = image_details.find({
#         "photo_id": int(image_id)  # Replace with variable
#     })
#     for x in photo_details:
#         return x
    
def get_image(image_id):
    cursor = fsFilesColl.find({
        # '_id' : ObjectId(image_id)
        'metadata': {'photo_id': image_id}
    })
    for item in cursor:
        id = item['_id']
        new_img = fs.get(id)
        # base64_data = codecs.encode(new_img.read(), 'base64')
        # image = base64_data.decode('utf-8')
        encoded_file = base64.b64encode(new_img.read()).decode('utf-8')
        print(f'<img src="data:image/png;base64,{encoded_file}">')
        return encoded_file
    # <img src = "data:image/png;base64, {{image}}" alt= "myImage"/>
        
    
def main():
    image_id = "40430127283"
    #image_details = get_image_details(image_id)
    #print(image_details)
    get_image(image_id)

main()



