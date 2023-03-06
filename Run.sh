#!/bin/bash
python Initialize_Database.py
python statement.py
python direct_truths_only.py
python value_nodes.py
python name.py

python create_id.py
python meta_property.py
