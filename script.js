const connection = new Mongo( `mongodb://root:student@localhost:27017` ),
      db = connection.getDB( `Flickr` ),
      images = db.getCollection( `ImageDetails` )

// mongo import
// mongoimport --authenticationDatabase admin -u admin --db Flickr --collection Images --type csv --headerline --file Flickr_10k_dataset.csv
let cursor;

cursor = images.updateMany(
    { lon : { $exists: true} },
    [{ $set: { lon: { $toString: "$lon" } } }]
  );
print(cursor)

cursor = images.updateMany(
    { lat : { $exists: true} },
    [{ $set: { lat: { $toString: "$lat" } } }]
  );
print(cursor)

cursor = images.updateMany(
    {},
    [
        {
            $set: {
                lon: { 
                    $replaceOne: {
                        input: "$lon",
                        find: ",",
                        replacement: "."
                    }
                },
                lat: {
                    $replaceOne: {
                        input: "$lat",
                        find: ",",
                        replacement: "."
                    }
                }
            }
        }
    ]
);
print(cursor)

cursor = images.updateMany(
    {},
    [
        {
            $set: {
                lon: { 
                    $replaceAll: {
                        input: "$lon",
                        find: ",",
                        replacement: ""
                    }
                },
                lat: {
                    $replaceAll: {
                        input: "$lat",
                        find: ",",
                        replacement: ""
                    }
                }
            }
        }
    ]
);
print(cursor)


cursor = images.updateMany(
    {},
    [
        {
            $set: {
                lon: {
                    $cond: {
                        if: 
                            { $eq: ["$lon", 'NA']}
                        ,
                        then: null,
                        else: "$lon"
                    }
                }
            }
        }
    ]
);
print(cursor)

cursor = images.updateMany(
    {},
    [
        {
            $set: {
                lat: {
                    $cond: {
                        if: {
                            $eq: ["$lat", 'NA']
                        },
                        then: null,
                        else: "$lat"
                    }
                }
            }
        }
    ]
);
print(cursor)

cursor = images.updateMany(
    { lon : { $exists: true} },
    [{ $set: { lon: { $toDouble: "$lon" } } }]
  );
print(cursor)

cursor = images.updateMany(
    { lat : { $exists: true} },
    [{ $set: { lat: { $toDouble: "$lat" } } }]
  );
print(cursor)

cursor = images.updateMany(
    {},
    [
        {
            $set: {
                location: {
                    $cond: {
                        if: { $or: [
                            { $eq: ["$lon",null] },
                            { $eq: ["$lat",null] }
                        ]},
                        then: null,
                        else: {
                            type: 'Point',
                            coordinates: [ "$lon", "$lat"]
                        }
                    }
                }
            }
        },
        {
            $unset: [ 'lon', 'lat']
        }
    ]
);
print(cursor)


images.createIndex({location: `2dsphere`});