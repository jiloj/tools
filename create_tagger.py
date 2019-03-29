#!/usr/bin/env python

"""
The jtagger service requires for its training data a json object where the key
is the id of the clue on the jnode service, and the value is the semantic
category label. Other information is required as well to create a proper new
tagger. This process is abstracted and automated in this script.
"""

import argparse
import csv

import requests


FIELDNAMES = ['id', 'category', 'question', 'answer', 'round', 'value', 'semanticcategory']
JTAGGER_CREATE_TAGGER_URL = 'http://localhost:9001/taggerrefs/'


parser = argparse.ArgumentParser()
parser.add_argument('data', help='The input file name with the annotated data.')
parser.add_argument('name', help='The name of the to be created tagger.')
args = parser.parse_args()


annotated_data = {}
with open(args.data, newline='') as input_f:
    reader = csv.DictReader(input_f)

    for row in reader:
        clue_id = row['id']
        cat = row['semanticcategory']

        if cat:
            annotated_data[clue_id] = cat

resp = requests.post(JTAGGER_CREATE_TAGGER_URL, json = {
    'name': args.name,
    'data': annotated_data
})

try:
    resp.raise_for_status()
    j = resp.json()

    if j['success']:
        print('Tagger created successfully.')
    else:
        print('Tagger not created succesfully. Response printed below.')
        print(resp.text)
except requests.exceptions.HTTPError as e:
    print('Error in tagger creation request response.')
    print(e)
