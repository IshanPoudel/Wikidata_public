''' The two tables that are here are

properties 
entities


'''

'''
1. Reads the file

2. Calls the store_name function
2a. When store_name function gets called with the key Q , it looks for all values 
  with <http://www.wikidata.org/entity/Q.*> <http://schema.org/name> .*@en .$
  We are only looking for english values.
  Then for each Q[0-9]* value , we start with descripton

3. When the store_name function gets called with the key P , it looks for all values 
   with <http://www.wikidata.org/entity/P.*> <http://schema.org/name> .*@en .$
   We are only looking for english values.
   Then for each P[0-9]* value , we start with descripton


'''

import re
import mysql.connector
# //READ FILE


import json

f = open('database_config.json')
data = json.load(f)



db = mysql.connector.connect(host=data['host'],
                             user=data['user'],
                             passwd=data['password'],
                             database="wikidata")


mycursor = db.cursor()

property_query = "INSERT INTO properties (property , name , description) VALUES (%s , %s , %s )"
entity_query = "INSERT INTO entities (entity , name , description) VALUES (%s , %s , %s)"
# mycursor.execute("CREATE TABLE properties(property VARCHAR(30) , name VARCHAR(1000) )")


# When working this on the original file , use filepath instead of prop+filepath
file1 = open(data['filepath'], 'r')
Lines = file1.readlines()

file2= open(data['filepath'], 'r')
Lines_2 = file2.readlines()

def store_name(Lines , char):
    for line in Lines:
        x = re.search("<http://www.wikidata.org/entity/"+char+".*> <http://schema.org/name> .*@en .$", line)

        if x:
            arr = line.split(">")
            identifier = re.split("/", arr[0], 4)[-1]
            name = arr[2][0:-6]  # to remove [0:-2]



            for value in Lines:

                search_pattern = "<http://www.wikidata.org/entity/" + identifier + "> <http://schema.org/description>.*@en .$"
                y = re.search(search_pattern, value , re.IGNORECASE)
                label = "NULL"
                if y:
                    label = re.split("/description> ", value, 1)[-1][0:-6]

                    break

            if char == 'P':
                query = property_query
            else:
                query = entity_query
            try:
                mycursor.execute(query, (identifier , name , label))
                db.commit()

            except Exception  as e:
                print(e)

store_name(Lines , "P" )
store_name(Lines_2 , "Q" )






