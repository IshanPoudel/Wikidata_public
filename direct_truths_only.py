
''' The three tables that are stored are

1) store_entity_property_statement_triple() stores entity , property ,
statement triple which links entity through a predicate to its statement entity node aka  q-312-345
in the entity_property_statement_triple table

2) store_direct_truths() function stores statement  ,property and direct truth (can be an entity or a wikidata custom type) 
in the direct_truth_triple table.

3) store_statement_id() function stores each unique statement in the statement_id table.


'''

import re
import mysql.connector

import json





def store_statement_id():

    '''We index all unique statement nodes in a separate table'''
    
    mycursor.execute("INSERT INTO statement_entity_id ( statement_entity) SELECT DISTINCT statement_entity FROM entity_property_statement_triple")


def store_entity_property_statement_triple(char):

    ''' We link entities and theri properties with their statement nodes.

      <Q31><P1082><Q31-3CC82F14-06C3-4B4F-9512-695E4121A252> '''


    query = "INSERT INTO entity_property_statement_triple (entity ,property , statement_entity) VALUES (%s , %s , %s)"

    arr = char.split()

    arr[0] = re.split("/" , arr[0] , 4)[-1]
    arr[0] = arr[0][0:-1]  #to remove the '>' at the end

    #check 2nd value for property
    check_for_prop = re.search("^<http://www.wikidata.org/prop/P" , arr[1] , flags=re.IGNORECASE)

    if check_for_prop:


        arr[1] = re.split("/", arr[1], 4)[-1]
        arr[1] = arr[1][0:-1]

        # to get the entity value
        arr[2] = re.split("/", arr[2], 5)[-1]
        arr[2] = arr[2][0:-1]
        try:
            mycursor.execute(query, (arr[0], arr[1] , arr[2]))
            db.commit()


        except:
            print("Could not insert " + arr[0] + " " + arr[1] + " " + arr[2])

        return True, arr



    return False, arr




def store_direct_truths(char):
    ''' For each entity looks for <Q31><prop/direct/P20><Q40> , and stores it in direct_truth_triple table '''
    ''' We only look at Q31-P25-Q31 . We do not want any simple string in the final value'''

    query = "INSERT INTO direct_truth_triple (entity , property , value) VALUES (%s , %s , %s) "



    arr= char.split(">")
    check_for_direct_prop = re.search("^ <http://www.wikidata.org/prop/direct/P", arr[1] , flags=re.IGNORECASE)

    arr[0] = re.split("/", arr[0], 4)[-1]
    arr[0] = arr[0]  # to remove the '>' at the end

    arr[1] =re.split("/" , arr[1] , 5)[-1]

    if check_for_direct_prop:


        #check_if_direct_property_leads_to_an_entity
        check_if_entity = re.search(" <http://www.wikidata.org/entity/Q", arr[2] , flags=re.IGNORECASE)
        if check_if_entity:
            arr[2] = re.split("/" , arr[2] , 4)[-1]
            
            try:

                mycursor.execute(query, (arr[0], arr[1], arr[2]))
                db.commit()
                # print("I inserted " + arr[0] + " " + arr[1] + " " + arr[2])
            except:
                a=1
                # print("Could not insert " + arr[0] + " " + arr[1] + " " + arr[2])
            return True , arr


    return False , arr




f = open('database_config.json')
data = json.load(f)



db = mysql.connector.connect(host=data['host'],
                             user=data['user'],
                             passwd=data['password'],
                             database="wikidata")


mycursor = db.cursor()




# Read the file
file1 = open(data['filepath'], 'r')
Lines = file1.readlines()

#have an array with only entity values . Values starting from Q[0-9]*
Matched=[]

for line in Lines:
    x = re.search("^<http://www.wikidata.org/entity/Q[0-9]*>", line)
    if x:
        Matched.append(line)


for line in Matched:
    test , arr = store_entity_property_statement_triple(line)


store_statement_id()




#Insert direct truths
for line in Matched:
    test , arr = store_direct_truths(line)










