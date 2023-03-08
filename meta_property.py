''' Store all properties in a single table
After the whole file is filled , we can take a look at possible metaproperties.'''

import mysql.connector
import re

import json

f = open('database_config.json')
data = json.load(f)



db = mysql.connector.connect(host=data['host'],
                             user=data['user'],
                             passwd=data['password'],
                             database="wikidata")

mycursor = db.cursor()

#just get everything from one file.

file1 = open(data['filepath'], 'r')


query = 'INSERT INTO master_properties (property , edge , meta_property) VALUES (%s , %s , %s)'

for line in file1.readlines():

    x = re.search("^<http://www.wikidata.org/entity/P", line)
    # Parse it into three different.
    if x:

        arr = line.split()
        arr[0] = arr[0].split('entity/')
        arr[0] = arr[0][-1][:-1]
        # print(arr[0] , arr[1] , arr[2])
        mycursor.execute(query , (arr[0] , arr[1] , arr[2]))
        db.commit()

# mycursor.execute("ALTER TABLE entities RENAME COLUMN entity_id to ID , RENAME COLUMN entity to wikidata_id")
# mycursor.execute("ALTER TABLE properties RENAME COLUMN property_id to ID , RENAME COLUMN property to wikidata_id")
# db.commit()
