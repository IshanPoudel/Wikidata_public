'''Stores value_nodes in a tables titled value_nodes

Value_node contains a value (e63b83822...)
The possible predicates are: 
    rdf-syntax-ns#type - States the type of the object (Time , GlobecoordinateValue)

Based on the predicate the valuen node may further contain:
     geolatiude - Stores the latitude in the format <Number><Data_type> 
         Data_type may be double 
         
'''



import re

#get syntax type and the associated units
import mysql.connector

import json

f = open('database_config.json')
data = json.load(f)



db = mysql.connector.connect(host=data['host'],
                             user=data['user'],
                             passwd=data['password'],
                             database="wikidata")

mycursor = db.cursor()

query = "INSERT INTO value_nodes (value_node , predicate , object) VALUES (%s , %s , %s)"


def store_value_nodes(line):
    arr = line.split()

    arr[0] = re.split("/" , arr[0] , 4)[-1][0:-1]
    # print(arr)


    if ("rdf-syntax-ns#type" in arr[1]):
        # get the type
        arr[1] = 'rdf-syntax-ns#type'
        arr[2] = re.split("ontology#" , arr[2] , 1)[-1][0:-1]
        return True , arr
    check_if_quantity_unit = re.search("<http://wikiba.se/ontology#quantityUnit>" , arr[1])
    if check_if_quantity_unit:
        arr[1] = 'quantityUnit'
        #get entity
        check_if_entity = re.search("^<http://www.wikidata.org/entity/" , arr[2])
        if check_if_entity:
            arr[2] = re.split("/" , arr[2] , 4)[-1][0:-1]
            arr[2] = "<entity>"+arr[2]
            return True ,arr
    # check_if_value_with_data_type
    if "^^<http://www.w3.org/2001/XMLSchema#" in arr[2]:
        arr[1] = re.split("ontology#" , arr[1] , 1 )[-1][:-1]
        temp = arr[2].split("^^")
        value = temp[0]
        data_type = temp[1]
        # //get the data type value
        data_type = re.split("#", data_type, 1)[-1][:-1]
        # get the first value first.
        arr[2] = value + "<" + data_type + ">"
        return True , arr

    return False , arr


file1 = open(data['filepath'], 'r')



for line in file1.readlines():
    x = re.search("^<http://www.wikidata.org/value/" , line)
    # we get only values that are wikidata entities
    arr=[]
    #Initialize array_list
    if x:


        test , arr  = store_value_nodes(line)
        if test:

            # store to database




            try:
                mycursor.execute(query , (arr[0] , arr[1] , arr[2]))
                db.commit()
                # print("Inserted into database")
            except Exception as e :
                print("Could not insert " + arr[0] + " " +arr[1] + " "+ arr[2])
                print(e)

