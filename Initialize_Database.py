import mysql.connector


import json

f = open('database_config.json')
data = json.load(f)



db = mysql.connector.connect(host=data['host'],
                             user=data['user'],
                             passwd=data['password'],
                             database="wikidata")




mycursor = db.cursor()


mycursor.execute("DROP database if exists wikidata ")
mycursor.execute("CREATE database wikidata")

db = mysql.connector.connect(host="localhost",
                             user="root",
                             passwd="rootroot",
                             database="wikidata")

mycursor = db.cursor()



mycursor.execute("CREATE TABLE properties(property_id int PRIMARY KEY AUTO_INCREMENT ,  property VARCHAR(30) , name VARCHAR(500) , description VARCHAR(1000))") #done

mycursor.execute("CREATE TABLE entities(entity_id int PRIMARY KEY AUTO_INCREMENT ,entity VARCHAR(30) , name VARCHAR(500) , description VARCHAR(1000))") #done

mycursor.execute("CREATE TABLE direct_truth_triple(entity VARCHAR(30), property VARCHAR(30) , value VARCHAR(1000) )")


mycursor.execute("CREATE TABLE statement_triple (entity VARCHAR(50) , property VARCHAR(100) , statement VARCHAR(1000) )") #done

mycursor.execute("CREATE TABLE entity_property_statement_triple (entity VARCHAR(30) , property VARCHAR(100) , statement_entity VARCHAR(150) )") #done

mycursor.execute("CREATE TABLE value_nodes (value_node VARCHAR(50) , predicate VARCHAR(50) , object VARCHAR(50) )")#done

mycursor.execute("CREATE TABLE statement_entity_id (statement_entity_id int PRIMARY KEY AUTO_INCREMENT , statement_entity VARCHAR(150))")

mycursor.execute("CREATE TABLE prop_statements_and_qualifiers_id (property_id int PRIMARY KEY AUTO_INCREMENT , property VARCHAR(150))")
#No use

mycursor.execute("CREATE TABLE master_properties (property_id int PRIMARY KEY AUTO_INCREMENT , property VARCHAR(30) , edge VARCHAR(1000) , meta_property VARCHAR(1000)) ")

mycursor.execute("CREATE TABLE statement_property_types ( ID int PRIMARY KEY AUTO_INCREMENT ,  type VARCHAR(30))")

mycursor.execute("CREATE TABLE property_and_qualifiers ( ID int NOT NULL PRIMARY KEY AUTO_INCREMENT , name VARCHAR(500) ,property_qualifier VARCHAR(100) , property_id INT , property_type INT ,FOREIGN KEY (property_id) REFERENCES properties(property_id) , FOREIGN KEY (property_type) REFERENCES statement_property_types(ID))")
# select e.entity_id as subject_id , p.property_id as property_id , e2.entity_id as object_id  from direct_truth_triple dt JOIN properties p ON dt.property = p.property JOIN entities e ON e.entity = dt.entity JOIN entities e2 on e2.entity=dt.entity LIMIT 10

mycursor.execute("CREATE TABLE statement_triples (Statement INT , PROPERTY INT , Entity INT , property_type INT) ")
# No use
