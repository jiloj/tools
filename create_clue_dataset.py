#!/usr/bin/env python

"""
Produces a dataset for annotation from the jnode service. This polls the /clues
endpoint on the jnode service and parses the json output and outputs a csv file
that can be easily annotated.
"""

import argparse
import csv
import random
import sys

import requests


JNODE_CLUES_URL = 'http://localhost:9000/clues/'
FIELDNAMES = ['id', 'category', 'question', 'answer', 'round', 'value', 'semanticcategory']


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='The name of the output filename')
parser.add_argument('-r', '--random', action='store_true',
        help='Whether the output order of clues should be random.')
args = parser.parse_args()

resp = requests.get(JNODE_CLUES_URL)
clues = resp.json()

if args.random:
    random.shuffle(clues)

with open(args.filename, 'w', newline='') as f:
    cluewriter = csv.DictWriter(f, FIELDNAMES)
    cluewriter.writeheader()

    for clue in clues:
        cluewriter.writerow(clue)
