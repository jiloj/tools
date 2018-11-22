#!/usr/bin/env python

"""
Tranfers annotations from one annotated dataset to another. These files are in
csv format, but the ids of the clues are not guaranteed to be the same between
files.
"""

import argparse
import csv
import random


def row_to_key(row):
    """
    Convert a row to its key, a unique value specific to that row.

    Args:
        row: The row to convert to a key.

    Returns:
        The key for the row.
    """
    return (row['category'], row['question'], row['answer'], row['round'], row['value'])


def row_to_dict(row):
    """
    Creates a copy of the row as a dict.

    Args:
        row: The row to make a copy of.

    Returns:
        The copied / transferred dictionary.
    """
    return {
        'id': row['id'],
        'category': row['category'],
        'question': row['question'],
        'answer': row['answer'],
        'round': row['round'],
        'value': row['value'],
        'semanticcategory': row['semanticcategory']
    }


FIELDNAMES = ['id', 'category', 'question', 'answer', 'round', 'value', 'semanticcategory']


parser = argparse.ArgumentParser()
parser.add_argument('source', help='The source file of the annotations')
parser.add_argument('destination',
        help='The destination file of the annotations.')
parser.add_argument('output',
        help='Location to output the results of the transfer.')
args = parser.parse_args()

source_annotations = {}
with open(args.source, newline='') as source_f:
    source_reader = csv.DictReader(source_f, FIELDNAMES)

    for row in source_reader:
        if row['semanticcategory']:
            source_annotations[row_to_key(row)] = row['semanticcategory']

annotated_rows = []
rest_rows = []
with open(args.destination, newline='') as destination_f:
    destination_reader = csv.DictReader(destination_f, FIELDNAMES)

    for row in destination_reader:
        d = row_to_dict(row)
        try:
            cat = source_annotations[row_to_key(row)]
            d['semanticcategory'] = cat
            annotated_rows.append(d)
        except KeyError:
            rest_rows.append(d)

with open(args.output, 'w', newline='') as output_f:
    writer = csv.DictWriter(output_f, FIELDNAMES)

    for row in annotated_rows:
        writer.writerow(row)

    random.shuffle(rest_rows)

    for row in rest_rows:
        writer.writerow(row)
