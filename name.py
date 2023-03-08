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




mycursor.execute("CREATE TABLE entities_name_only(entity VARCHAR(30) , name VARCHAR(500) )")
mycursor.execute("CREATE TABLE property_name_only(property VARCHAR(30) , name VARCHAR(500) )")


query_entity = "INSERT INTO entities_name_only(entity , name) VALUES(%s ,%s)"
query_property = "INSERT INTO property_name_only(property , name) VALUES (%s , %s)"

def store_entity_name(char):

    file1 = open(data['filepath'], 'r')

    for line in file1.readlines():

        if re.search("<http://www.wikidata.org/entity/"+char+".*> <http://schema.org/name> .*@en .$", line):
            arr = line.split(">")
            identifier = re.split("/", arr[0], 4)[-1]
            name = arr[2][0:-6]  # to remove [0:-2]
            try:
                if char == "Q":
                    mycursor.execute(query_entity, (identifier , name))
                    # print(identifier , name)
                else:
                    mycursor.execute(query_property, (identifier, name))


                db.commit()

            except Exception  as e:
                print(e)
    file1.close()


store_entity_name("Q")
print("Entity name done")
store_entity_name("P")
print("Property name done")

# def store_entity_description(char):
#     for line in file1.readlines():
#         x = re.search("<http://www.wikidata.org/entity/P[0-9].> <http://schema.org/description>.*@en .$" , line , re.IGNORECASE)
#         if x:



# Create table for entity_description and property_description
mycursor.execute("CREATE TABLE entities_dcp_only(entity VARCHAR(30) , description VARCHAR(500) )")
mycursor.execute("CREATE TABLE property_dcp_only(property VARCHAR(30) , description VARCHAR(500) )")

query_entity_d = "INSERT INTO entities_dcp_only(entity , description) VALUES(%s ,%s)"

query_property_d = "INSERT INTO property_dcp_only(property , description) VALUES (%s , %s)"
def store_entity_description():
    # print("This file is called")
    file1 = open(data['filepath'], 'r')
    for line in file1.readlines():
        x = re.search("<http://www.wikidata.org/entity/Q.*> <http://schema.org/description> .*@en .$" , line , re.IGNORECASE)
        if x:
            arr = line.split(">")
            identifier = re.split("/", arr[0], 4)[-1]
            #Get the description
            label = re.split("/description> ", line, 1)[-1][0:-6]
            mycursor.execute(query_entity_d , (identifier , label))
            db.commit()

    file1.close()




def store_property_description():
    # print("This file is called")
    file1 = open(data['filepath'], 'r')
    for line in file1.readlines():
        x = re.search("<http://www.wikidata.org/entity/P.*> <http://schema.org/description> .*@en .$", line, re.IGNORECASE)
        if x:
            arr = line.split(">")
            identifier = re.split("/", arr[0], 4)[-1]
            # Get the description
            label = re.split("/description> ", line, 1)[-1][0:-6]
            mycursor.execute(query_property_d, (identifier, label))
            db.commit()
    file1.close()


store_entity_description()
print("Entity description done")
store_property_description()
print("Property description done")

mycursor.execute("INSERT INTO entities (entity , name , description) select en.entity , en.name , ed.description from entities_name_only en JOIN entities_dcp_only ed ON en.entity=ed.entity")
mycursor.execute("INSERT INTO properties (property , name , description) select pn.property , pn.name , pd.description from property_name_only pn JOIN property_dcp_only pd ON pn.property=pd.property")
db.commit()
