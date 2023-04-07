import base64
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient, TEXT
from bson import ObjectId
import gridfs

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://root:student@localhost:27017")
db = client['Flickr']
collection = db['ImageDetails']
fs = gridfs.GridFS(db)
fsFilesColl = db["fs.files"]

# Create a text index for search
collection.create_index([("content", TEXT)])

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    area = request.form.get("area")
    search_result = collection.find({"title": {"$regex": query}})

    if area:
        lat, lon = map(float, area.split(","))
        max_distance = 10000  # 10 kilometers
        search_result = collection.find({
            "title": {"$regex": query, "$options": "i"},
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
    else:
        results = [{'_id': str(r['_id']), 'title': r['title'], 'date': r['taken']} for r in search_result]

    return jsonify(list(results))


@app.route("/ImageDetails/<string:doc_id>")
def document(doc_id):
    doc = collection.find_one({"_id": ObjectId(doc_id)})
    if not doc:
        return "Document not found", 404
    photo_id = doc['photo_id']
    cursor = fsFilesColl.find({
        'metadata': {'photo_id': str(photo_id)}
    })
    for item in cursor:
        id = item['_id']
        new_img = fs.get(id)
        encoded_file = base64.b64encode(new_img.read()).decode('utf-8')
        return render_template('ind.html', title=doc['title'], description=doc['description'], city=doc['u_city'], country=doc['u_country'], imga = encoded_file)


if __name__ == '__main__':
    app.run(debug=True)

