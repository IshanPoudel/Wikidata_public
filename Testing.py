# Check if property and qualifier statements only consists of <entities>
# select * from statement_triple WHERE property REGEXP '^QUALIFIER/P|prop/statement/P' and statement NOT REGEXP '^<entity>' ;

# select i.property from prop_statements_and_qualifiers_id as i JOIN statement_triple as st ON i.property=st.property WHERE st.statement NOT REGEXP '^<entity>'
