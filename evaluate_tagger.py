#!/usr/bin/env python

"""
An evaluation of a jtagger service tagger. This script takes in the name of the
tagger, and the data to evaluate on. The resulting output will display the
accuracy.
"""

import argparse
import random

import requests

import data
import jtagger


"""
The url to post against for tagging.
"""
JTAGGER_TAG_URL = 'http://localhost:9001/tag'


parser = argparse.ArgumentParser()
parser.add_argument('data', help='The dataset to evaluate the tagger on.')
parser.add_argument('name', help='The name of the tagger to evaluate.')
args = parser.parse_args()

correct = 0
total = 0

dataset = data.load_dataset_from_csv(args.data)
for item in dataset:
    r = int(item.round)
    v = int(item.value)
    guess = jtagger.tag(args.name, item.category, item.question, item.answer, r, v)
    actual = item.semanticcategory

    correct += int(actual.lower() == guess.lower())
    total += 1

print(correct / total)
