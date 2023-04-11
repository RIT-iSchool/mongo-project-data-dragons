[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=10442800&assignment_repo_type=AssignmentRepo)


DataSet - 
Flickr 10k Dataset 
https://www.kaggle.com/datasets/amiralisa/flickr?resource=download


* Fields available in the csv file: 

---------------------------------------------------------
| Field        | Description                            |
| ------------ | -------------------------------------- |
| photo_id     | ID of the photo                        |
| owner        | User ID of the photo owner             |
| gender       | Gender of the photo owner              |
| occupation   | Occupation of the photo owner          |
| title        | Title of the photo                     |
| description  | Description of the photo               |
| faves        | Favorite rate of the photo             |
| lat          | Latitude of the photo                  |
| lon          | Longitude of the photo                 |
| u_city       | City of the photo owner                |
| u_country    | Country of the photo owner             |
| taken        | Time the photo was taken               |
| weather      | Weather condition at the time of photo |
| season       | Season at the time of the photo        |
| daytime      | Time of day the photo was taken        |
---------------------------------------------------------

* Downloaded data was in a csv file(converted to UTF-8 for ingestion because it had unicode data in it. )

* Imported the database using the mongo import command in cmd.
    Command: mongoimport --authenticationDatabase admin -u admin --db Flickr --collection Images --type csv --headerline --file Flickr_10k_dataset.csv


Script.js: (We have used this script for installing the csv file of flickr dataset)

    1. Converted the lat and lon fields to string for manipulation. {lat & lon:(36,861,544	-5,177,747),(51,463,766	5,392,935)}.
        a. replace commas with dots.
        b. remove the remaining commas.
        c. convert the lat and lon fields to numbers again.
    2. Created a new "location" field that contains a GeoJSON Point object with the "lon" and "lat" coordinates, and removes the "lon" and "lat" fields.
    3. Creates a 2dsphere index on the "location" field.

Tech Stack:
1. Mongo: To store data and image objects
2. Python: For data access. Teamvote.
3. Flask: Since it is seamless with python. 
4. html: For UI













RLES Machine Details:
192.168.192.176

DB Name -  Flickr
Collections - ImageDetails
Images present in fs.files and fs.chunks

