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


"""
The url to post against for tagging.
"""
JTAGGER_TAG_URL = 'http://localhost:9001/tag'


def tag(name, category, question, answer, r, v):
    """
    Tag a given question with a given tagger.

    Args:
        name: The name of the tagger to use.
        category: The category of the data item.
        question: The question text of the data item. What user sees.
        answer: The answer text of the data item. What user responds.
        r: The integral round that the clue is in. Between 1 and 4.
        v: The integral value of the clue from 0 to 5.

    Returns:
        The semantic category of the item as a string.
    """
    clue = {
        'category': category,
        'question': question,
        'answer': answer,
        'round': r,
        'value': v
    }

    resp = requests.post(JTAGGER_TAG_URL, json = {
        'tagger': name,
        'clue': clue
    })

    resp.raise_for_status()
    j = resp.json()
    return j['semanticcategory']


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
    guess = tag(args.name, item.category, item.question, item.answer, r, v)
    actual = item.semanticcategory

    correct += int(actual.lower() == guess.lower())
    total += 1

print(correct / total)
