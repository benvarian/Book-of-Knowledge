# Book-of-Knowledge

## Team 
- Ben Varian: 23210549 
- Mitchell Otley: 23475725

## Setup python environment
1. Make a python virtual environment
```bash
python3 -m venv venv
```
2. install dependencies
```bash
pip install -r requirements.txt
```
3. Activate environment (Linux + MacOS)
```bash
source venv/bin/activate
```
4. Activate environemnt (Windows)
```powershell
venv\Scripts\Activate.ps1
```

## How to run web crawlers

1. Navigate to the scraping_results folder
```bash
cd scraping_results
```
2. run major crawler 
```bash
python3 unit-crawler.py
```
3. run unit crawler 
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

## How to run queries 

All of our queries are stored in one file and will print the results to the standard output.

```bash
python3 queries.py
```

## How to run SHACL validation 
The commands for the shacl validation are stored in the `shacl_validate.py` file. To run this file please run
``` bash 
python3 shacl_validate.py
```