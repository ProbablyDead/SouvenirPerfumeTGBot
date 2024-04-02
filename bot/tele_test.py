import json

PATH = "./data/test.json"

with open(PATH, 'r') as js:
    test = json.load(js)

QUESTION_COUNT = len(test) 
INGREDIENT_QUESTION_COUNT = len([item for item in test if item['ingredients']]) 
