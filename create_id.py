# create id for direct_truth
import mysql.connector
import json

f = open('database_config.json')
data = json.load(f)



db = mysql.connector.connect(host=data['host'],
                             user=data['user'],
                             passwd=data['password'],
                             database="wikidata")

mycursor = db.cursor()

#Table for direct_truth_triple in id form
query = "create table direct_truth_triple_id as select e.entity_id as subject_id , p.property_id as property_id , e2.entity_id as object_id from direct_truth_triple dt JOIN entities e on e.entity=dt.entity JOIN properties p on dt.property=p.property JOIN entities e2 on e2.entity=dt.value"
mycursor.execute(query)
db.commit()


#Table for entity-property-statement_node in id form
query = "create table entity_property_statement_triple_in_id_form select e.entity_id , p.property_id , s.statement_entity_id from entity_property_statement_triple st JOIN entities e on st.entity=e.entity JOIN properties p ON  st.property=p.property JOIN statement_entity_id s on st.statement_entity = s.statement_entity"
#create id for statement_triple table
mycursor.execute(query)
db.commit()

#Table for statment-node - property -entity not in id form
query = "CREATE TABLE statement_triple_clean SELECT entity , property , SUBSTRING_INDEX(statement , '<entity>' , -1) AS value from statement_triple where property REGEXP '^prop/statement/P[0-9]*|qualifier/P[0-9]*' AND  statement  REGEXP '^<entity>'"
mycursor.execute(query)
db.commit()



#Table for having property from statement node - property name - propety_id - property_type(Either direct prop or a qualifier)
mycursor.execute("INSERT INTO property_and_qualifiers (name, property_qualifier, property_id, property_type) \
                  SELECT DISTINCT SUBSTRING(st.property,16), st.property, p.property_id, 1 \
                  FROM statement_triple_clean st \
                  JOIN properties p ON SUBSTRING(st.property,16) = p.property \
                  WHERE st.property REGEXP '^prop/statement'")
db.commit()

mycursor.execute("INSERT INTO property_and_qualifiers (name, property_qualifier, property_id, property_type) \
                  SELECT DISTINCT SUBSTRING(st.property,11), st.property, p.property_id, 2 \
                  FROM statement_triple_clean st \
                  JOIN properties p ON SUBSTRING(st.property,11) = p.property \
                  WHERE st.property REGEXP '^qualifier/P'")
db.commit()





# No use
mycursor.execute("CREATE TABLE statement_ids_from_statement_triples(id int PRIMARY KEY AUTO_INCREMENT , statement VARCHAR(1000) ) ")
query = "INSERT INTO statement_ids_from_statement_triples(statement) SELECT distinct statement from statement_triple WHERE property REGEXP '^prop/st|qualifier/P'"
mycursor.execute(query)
db.commit()






#Final table for statement node -property-entity
query="CREATE TABLE statement_triples_in_id_form AS SELECT sid.statement_entity_id AS statement, p.property_id AS property, e.entity_id AS entity, p.property_type AS property_type FROM statement_triple_clean stc JOIN statement_entity_id sid ON sid.statement_entity = stc.entity JOIN entities e ON e.entity = stc.value JOIN property_and_qualifiers p ON p.name = stc.property"
mycursor.execute(query)

db.commit()