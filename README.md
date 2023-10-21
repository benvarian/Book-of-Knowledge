# Book-of-Knowledge

## Team 
- Ben Varian: 23210549 
- Mitchell Otley: 23475725

## How to run web crawlers

1. Make a python virtual environment
```bash
python3 -m venv venv
```
2. install dependencies
```bash
pip install -r requirements.txt
```
3. Navigate to the scraping_results folder
```bash
cd scraping_results
```
4. run major crawler 
```bash
python3 unit-crawler.py
```
5. run unit crawler 
```bash
python3 unit-crawler.py
```

## How to create the knowledge graph + OWL file
1. Navigate back to the root directory of the project
```bash
cd ..
```
2. Run the create graph file
```bash
python3 create_graph.py
```
Upon successful completion this will create the handbook.ttl file in the root directory of the project.

3. Populate the owl file with the rules and axioms
```bash
python3 create_onto.py
```
4. Load all the data into the ontology
```bash
python3 load_onto.py
```