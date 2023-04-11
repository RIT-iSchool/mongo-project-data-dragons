[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=10442800&assignment_repo_type=AssignmentRepo)


DataSet - 
Flickr 10k Dataset 
https://www.kaggle.com/datasets/amiralisa/flickr?resource=download

* Downloaded data was in a csv file(converted to UTF-8 for ingestion because it had unicode data in it. )


* Fields available in the csv file: 
Flickr Dataset
---------------------
Data fields:

photo_id \
owner -> user id related to the owner of the photo \
gender -> owner's gender \
occupation -> occupation of owner \
title -> title of photo \
description -> description of photo \
faves -> photo's favorite rate \
lat -> photo's latitude \
lon -> photo's longitude \
u_city -> user's city \
u_country -> user's country \
taken -> the time of photo taken \
weather -> weather condition related to the time that photo is taken \
season -> season related to the time that photo is taken \
daytime -> time of the day that photo is taken 
---------------------

* Imported the database using the mongo import command in cmd.
    Command: mongoimport --authenticationDatabase admin -u admin --db Flickr --collection Images --type csv --headerline --file Flickr_10k_dataset.csv


Script.js: (We have used this script for installing the csv file of flickr dataset)

    1. Converted the lat and lon fields to string for manipulation. {lat & lon:(36,861,544	-5,177,747),(51,463,766	5,392,935)}.
        a. replace commas with dots.
        b. remove the remaining commas.
        c. if null replace with "NA".
        d. convert the lat and lon fields to numbers again.
    2. Created a new "location" field that contains a GeoJSON Point object with the "lon" and "lat" coordinates, and removes the "lon" and "lat" fields.
    3. Creates a 2dsphere index on the "location" field.

Tech Stack:
1. Mongo
2. Flask for creating the front end
3. Python for data access















RLES Machine Details:
192.168.192.176

DB Name -  Flickr
Collections - ImageDetails
Images present in fs.files and fs.chunks

