''' store_property_statements_and_qualifiers_id()
function stores all unique properties (prop/statement ) and qualifiers
in a table called prop_statements_and_qualifiers_id.'''


import re
import mysql.connector



def get_values( line):

    '''For each statement node , there can be multiple schema in the second part. 

      Statement nodes may have the following:
      the rank of the statement : <http://wikiba.se/ontology#rank

      link to the direct value itself : <http://www.wikidata.org/prop/statement/P"
              The linked value maybe an entity(starting with Q) , a value node (linking to a value node) , a simple string (need to grab the english value @en) or a custom wikidata value.
       
      statement_value : <http://www.wikidata.org/prop/statement/value/P  (Links to a value node)

      qualifier : <http://www.wikidata.org/prop/qualifier/P 
               Same as direct value itself . 

      qualifier value : <http://www.wikidata.org/prop/qualifier/value/P"  (Links to a value node)

      Given a line as input , it returns the statment correpsonding property and the value.
      
      Stores the output in the statement_triple (entity , property , statement) table.

      '''

    #need to split based not on white space


    arr = line.split(">")

    arr[0] = re.split("/" , arr[0] , 5)[-1]





    check_for_rank = re.search("^ <http://wikiba.se/ontology#rank" , arr[1] )

    check_for_statement = re.search("^ <http://www.wikidata.org/prop/statement/P" , arr[1])

    check_for_statement_value = re.search("^ <http://www.wikidata.org/prop/statement/value/P" , arr[1])

    check_for_qualifier = re.search("^ <http://www.wikidata.org/prop/qualifier/P" , arr[1])

    check_for_qualifier_value = re.search("^ <http://www.wikidata.org/prop/qualifier/value/P" , arr[1])

    if check_for_rank:
        arr[1] = "rank"
        arr[2] = re.split("#", arr[2], 1)[-1]
        return True, arr

    if check_for_statement:
        arr[1] = re.split("/", arr[1], 3)[-1]
        # //if an entity , grab the entity
        # //else grab the whole thing
        check_if_entity = re.search("<http://www.wikidata.org/entity/Q", arr[2], re.IGNORECASE)
        check_if_value = re.search("<http://www.wikidata.org/value/", arr[2], re.IGNORECASE)

        if "/XMLSchema#" in arr[2] or "/geosparql#wktLite" in arr[2]:
            temp = arr[2].split("^^")
            value = temp[0]
            data_type = temp[1]
            # //get the data type value
            data_type = re.split("#", data_type, 1)[-1]
            # get the first value first.
            arr[2] = "<" + data_type + ">" + value


        elif ("<http://commons.wikimedia.org/wiki/Special:FilePath") in arr[2]:
            return False, arr

        elif check_if_entity:
            arr[2] = re.split("/", arr[2], 4)[-1]
            arr[2] = "<entity>" + arr[2]

        elif check_if_value:
            arr[2] = re.split("/", arr[2], 3)[-1]


        else:

            # grab simple string
            arr[2] = arr[2][:-3]  # to remove ' ./n'
            # if the string ends in @ and two more chars , @en , @sx , grab only the english version.
            check_if_ends_with_language = re.search(".*@.*$", arr[2])

            if check_if_ends_with_language:

                check_if_ends_in_english = re.search(".*@en$", arr[2])

                if not check_if_ends_in_english:

                    return False, arr
                else:
                    arr[2] = arr[2][0:-3]
                    # remove @en from the end
        return True, arr

    if check_for_statement_value:
        arr[1] = re.split("/", arr[1], 4)[-1]
        arr[2] = re.split("/", arr[2], 4)[-1]
        return True, arr

    if check_for_qualifier:

        # print(arr)
        arr[1] = re.split("/", arr[1], 4)[-1]
        check_if_entity = re.search("<http://www.wikidata.org/entity/Q", arr[2], re.IGNORECASE)
        check_if_value = re.search("<http://www.wikidata.org/value/", arr[2], re.IGNORECASE)

        if "/XMLSchema#" in arr[2] or "/geosparql#wktLite" in arr[2]:

            temp = arr[2].split("^^")
            value = temp[0]
            data_type = temp[1]
            # //get the data type value
            data_type = re.split("#", data_type, 1)[-1]
            # get the first value first.
            arr[2] = "<" + data_type + ">" + value

        elif check_if_entity:
            arr[2] = re.split("/", arr[2], 4)[-1]
            arr[2] = "<entity>" + arr[2]

        else:
            # grab simple string
            arr[2] = arr[2][:-3]  # to remove ' ./n'
            # if the string ends in @ and two more chars , @en , @sx , grab only the english version.
            check_if_ends_with_language = re.search(".*@.*$", arr[2], re.IGNORECASE)
            if check_if_ends_with_language:
                check_if_ends_in_english = re.search(".*@en$", arr[2], re.IGNORECASE)
                if not check_if_ends_in_english:
                    return False, arr
                else:
                    arr[2] = arr[2][0:-3]  # remove @en from the end
        return True, arr

    if check_for_qualifier_value:
        arr[1] = re.split("/", arr[1], 4)[-1]
        arr[2] = re.split("/", arr[2], 4)[-1]
        return True, arr

    return False, arr

import json


f = open('database_config.json')
data = json.load(f)



db = mysql.connector.connect(host=data['host'],
                             user=data['user'],
                             passwd=data['password'],
                             database="wikidata")


mycursor = db.cursor()

query = "INSERT INTO statement_triple (entity , property , statement) VALUES (%s , %s , %s)"

file1 = open(data['filepath'], 'r')
Lines = file1.readlines()


#create files that match.
Matched=[]
for line in Lines:
    x = re.search("^<http://www.wikidata.org/entity/statement/q", line , flags=re.IGNORECASE)
    if x:
        # print(x)
        Matched.append(line)


for line in Matched:
    test , arr = get_values(line)
    if test:
        # print(arr)
        try:
            mycursor.execute(query, (arr[0], arr[1], arr[2]))
            db.commit()


        except Exception as e:
            print(e)






       # After you store everything , make a entity_statement_table with only property_qualifer.

#After creating the table , you need to create two tables , one with only entites.
#O
# query = "create table property_and_qualifiers as select property from statement_triple WHERE property REGEXP '^prop/statement/P|^qualifier/P' "
# mycursor.execute(query)
# db.commit()

# //from the property and qualifiers table ,join them with the property and qualifier using the if statement , first get the property and then qualifier.True

# //create table property and qualifier (id auto increment , property/qialifer varchar(100) , property_name , property_id);
# //first add all prop/statements.
# // then add all qualifiers.

# First add the two values in the statment_property_types.
mycursor.execute("INSERT INTO statement_property_types(type) VALUES ('prop/statement')")
mycursor.execute("INSERT INTO statement_property_types(type) VALUES ('qualifier')")
db.commit()


# Now fill the property_and_qualifiers_table with properties first and then statements.
# get the property name
#
# select  SUBSTRING(st.property,16), p.property_id  , 1 from statement_triple st  JOIN properties p ON SUBSTRING(st.property,16 ) = p.property  WHERE st.property REGEXP '^prop/statement'  LIMIT 10;
# select  SUBSTRING(st.property,11), p.property_id , 2  from statement_triple st  JOIN properties p ON SUBSTRING(st.property,11 ) = p.property  WHERE st.property REGEXP '^qualifier/P'  LIMIT 10;
# # qualifier.
# select st.entity , SUBSTRING(st.property,11), p.property_id , p.property , p.name  from statement_triple st  JOIN properties p ON SUBSTRING(st.property,11 ) = p.property  WHERE st.property REGEXP '^qualifier/P'  LIMIT 10;

# i have the substri

# insert into property_and_qualifiers



#One with the literals.

       #  select * from statement_triple WHERE property REGEXP '^prop/statement/P|prop/qualifier/P' and statement REGEXP '^<entity>' LIMIT 20;
       # select * from statement_triple WHERE property REGEXP '^prop/statement/P|prop/qualifier/P' and statement NOT REGEXP '^<entity>' LIMIT 20;
       #Just need  props and statements

# query = "CREATE TABLE statement_literals as select * from statement_triple WHERE property REGEXP '^prop/statement/P|^qualifier/P' and statement NOT REGEXP '^<entity>'"
# mycursor.execute(query)
# db.commit()


query = "CREATE TABLE statement_entities as select entity , property ,  SUBSTRING(statement,9) AS statement from statement_triple WHERE property REGEXP '^prop/statement/P|^qualifier/P' and statement REGEXP '^<entity>'"
mycursor.execute(query) 
db.commit()




       #  select s.statement from statement_entities s JOIN entities e ON e.entity=s.statement JOIN  properties p ON p.property = substring(s.property , 16)  LIMIT 2










       # //Split into 3 subject , predicate , object