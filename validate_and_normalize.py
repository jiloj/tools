#!/usr/bin/env python

"""
Utility script to validate and normalize a training set. This script will output
lines of invalidity, and will also normalize the training labels. Validation
errors will be output to stdout.
"""

import argparse
import csv


def validate(row, categories):
    """
    Validates a row against a given category.

    Args:
        row: The row that was read in to validate.
        categories: The semantic categories to validate against. These
            categories are all lowercased.
    """
    sc = row['semanticcategory'].lower()
    return sc or sc in categories


def display_invalid_info(row):
    """
    """
    print('Entry:')
    print('Question: {}'.format(row['question']))
    print('Answer: {}'.format(row['answer']))
    print('Invalid category: {}'.format(sc))


def normalize(row):
    """
    Normalize a input csv row.

    Currently this is simply lowercasing the semantic category.

    Args:
        row: The row to normalize.
    """
    row['semanticcategory'] = row['semanticcategory'].lower()


FIELDNAMES = ['id', 'category', 'question', 'answer', 'round', 'value', 'semanticcategory']
SEMANTIC_CATEGORIES = set(('history', 'sports', 'geography', 'culture', 'science', 'politics', 'religion', 'words', 'music', 'art', 'food', 'opera', 'literature', 'tv/film', 'theatre', 'classics'))


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='The input filename of the training set to validate.')
parser.add_argument('output', help='The file to output the new training set to.')
parser.add_argument('--strict', action='store_true', help='Keeps only validated rows')
args = parser.parse_args()

with open(args.filename, newline='') as read_f, open(args.output, 'w', newline='') as output_f:
    reader = csv.DictReader(read_f, FIELDNAMES)
    writer = csv.DictWriter(output_f, FIELDNAMES)

    for i, row in enumerate(reader):
        v = validate(row, SEMANTIC_CATEGORIES)
        if not v:
            display_invalid_info(row)

        if not args.strict or v:
            normalize(row)
            writer.writerow(row)
