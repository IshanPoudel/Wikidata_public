import mysql.connector

db = mysql.connector.connect(host='local' , 
                             user='ishan' , 
                             password = 'idirishan' , 
                             database = "wikidata_sample")

mycursor = db.cursor()

mycursor.execute("CREATE TABLE properties(property_id int PRIMARY KEY AUTO_INCREMENT ,  property VARCHAR(30) , name VARCHAR(500) , description VARCHAR(1000))") #done
db.commit()
print("Success")