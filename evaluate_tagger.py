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
import ml


"""
The url to post against for tagging.
"""
JTAGGER_TAG_URL = 'http://localhost:9001/tag'


parser = argparse.ArgumentParser()
parser.add_argument('data', help='The dataset to evaluate the tagger on.')
args = parser.parse_args()

correct = 0
total = 0

dataset = data.load_dataset_from_csv(args.data)
accuracies = ml.cross_validate(dataset, 10)
print(accuracies)
print(sum(accuracies) / len(accuracies))
