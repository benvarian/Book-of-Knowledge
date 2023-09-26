# Book-of-Knowledge

## How to run uni crawler
python is a pre-requisites to run file.

1. Make venv 
```bash
python -m venv venv
```
2. install dependencies
```bash
pip install -r requirements.txt
```
3. pick units that you want to analyse and fill in the unit-codes.txt file
4. run crawler
```bash
python unit-crawler.py
```
5. all output will be placed in units.json