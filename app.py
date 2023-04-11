import base64
from flask import Flask, redirect, render_template, request, jsonify, url_for
from pymongo import MongoClient, TEXT
from bson import ObjectId
import gridfs

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://appuser:appstudent@localhost:27017/Flickr")
db = client['Flickr']
collection = db['ImageDetails']
fs = gridfs.GridFS(db)
fsFilesColl = db["fs.files"]
comcoll = db['comment']

# Create a text index for search
# collection.create_index([("content", TEXT)])

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    area = request.form.get("area")
    search_result = collection.find({"title": {"$regex": fr"\b{query}\w*",  "$options": "i" }})
    if query and area:
    	
    	lat, lon = map(float, area.split(","))
    	max_distance = 10000  # 10 kilometers
    	search_result = collection.find({
    		"title": {"$regex": fr"\b{query}\w*", "$options": "i"},
    		"location": {
        		"$near": {
        			"$geometry": {
        				"type": "Point",
        				"coordinates": [lon, lat]
        			},
        			"$maxDistance": max_distance
        		}
		}})
    elif area:
        lat, lon = map(float, area.split(","))
        max_distance = 10000  # 10 kilometers
        search_result = collection.find({
            #"title": {"$regex": fr"\b{query}\w*", "$options": "i"},
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "$maxDistance": max_distance
                }
            }
        })
    
    results = [{'_id': str(r['_id']), 'title': r['title'], 'date': r['taken']} for r in search_result]

    return jsonify(list(results))


@app.route("/ImageDetails/<string:doc_id>")
def document(doc_id):
    doc = collection.find_one({"_id": ObjectId(doc_id)})
    if not doc:
        return "Document not found", 404
    photo_id = doc['photo_id']
    cursor = fsFilesColl.find_one({
        'metadata': {'photo_id': str(photo_id)}
    })
    if not cursor:
        print('In IF')
        cursor = fsFilesColl.find_one({
            'metadata': {'photo_id': 'default'}
            })
    print(cursor)

    id = cursor['_id']
    new_img = fs.get(id)
    encoded_file = base64.b64encode(new_img.read()).decode('utf-8')
    return render_template('ind.html', id=doc_id,title=doc['title'], occupation = doc['occupation'],description=doc['description'], city=doc['u_city'], country=doc['u_country'],imga = encoded_file)
    # for item in cursor:
    #     print(item)
    #     id = item['_id']
    #     new_img = fs.get(id)
    #     encoded_file = base64.b64encode(new_img.read()).decode('utf-8')
    #     return render_template('ind.html', id=doc_id,title=doc['title'], description=doc['description'], city=doc['u_city'], country=doc['u_country'],imga = encoded_file)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    comment_data = request.get_json()
    doc = collection.find_one({"_id": ObjectId(comment_data['_id'])})
    if not doc:
        return "Document not found", 404
    comcoll.update_one(
        {"photo_id": str(doc['photo_id'])}, 
        {"$push": {"comments": comment_data['comment']}}, 
        upsert=True
    )
    return jsonify({'comment': comment_data['comment']})

@app.route('/comments/<string:doc_id>')
def get_comments(doc_id):
    doc = collection.find_one({"_id": ObjectId(doc_id)})
    if not doc:
         return "Document not found", 404
    comment_present  = comcoll.find_one({
         "photo_id": str(doc['photo_id'])
     })
    if not comment_present:
        comments5 = []
    else:
        comments5 = str(comment_present['comments'])
    print(comments5)
    return jsonify({'comment': comment_present['comments']})

if __name__ == '__main__':
    app.run(debug=True)

