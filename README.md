# Wikidata_N_Triples_to_SQL

<h2>
  
Implements a local MySQL database for wikidata. 

Transforms raw wikidata dump in N-Triples form to a MySQL table.

Alternative to using the SPARQL endpoint of wikidata. 
  
</h2>

---

<h3> How to run </h3>

Update the db configuration in the configuration file.

	pip install -r requirements.txt
	run.sh




---

<h3> entities - Contains the name of the entity , its description and its unique identifier. </h3>


![Alt text](Assets/entity_name.png)

<h3> properties - Contains the name of the property , its description and its unique identifier. </h3>


![Alt text](Assets/property_name.png)

<h3> direct_truth_triple - Contains a triple of the entity , property and value. 

The value can be either a simple string , entity or a custom wikidata type.
It is in id form.


![Alt text](Assets/final_direct_truth_triples.png)



  
  
  ----

<h3> Statement_ids - Contains identifications for all wikidata statements.

![Alt text](Assets/statement_id.png)


  
<h3> Entity_Statements_triple - Contains triple of entity  , property and statement node . </H3>
 
Statement nodes are similar to CVT nodes in freebase. 
  
![Alt text](Assets/entity_property_statement_triple_in_id_form.png)
  
<h3> Statement_property_type - Denotes wether a property is a property statement edge type or a qualifier edge type.


 ![Alt text](Assets/statement_property_type.png)

 
 
 <h3> Statement_triples: Statement, property, entity, property_type (all in our ID form)

Yet to be added.
</h3>
 
 
 
 
 
   
   ----
   
  
   <h3> value_nodes - Contains value_nodes , the predicate and their values. </h3>
   
   
  ![Alt text](Assets/value_nodes.png)
  
   
  
 






