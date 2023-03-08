#!/bin/bash
python Initialize_Database.py
echo "Done Initializing"
python statement.py
echo "Statement.py done"
python direct_truths_only.py
echo "Direct_Truths_done"
python value_nodes.py
echo "Value_nodes_done"
python name.py
echo "Name done"

python create_id.py
echo "Create_id done"
python meta_property.py
echo "Meta_property done"
