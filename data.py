"""
Data utilities that are common across many scripts in the tools directory. This
includes functions such as reading csv data files, or common transformations or
validations of data.
"""

import csv

FieldNames = ['id', 'category', 'question', 'answer', 'round', 'value', 'semanticcategory']

class Expando:
    """
    A default expando class that can be added to as needed per object.
    """
    pass

def load_dataset_from_csv(filename):
    """
    Loads the dataset from a csv formatted file.

    Args:
        filename: The name of the file to load the data from. This file must
            at least have the headers defined in FieldNames.

    Returns:
        A list of the loaded data items, where each item is an object whose
        attributes are the FieldNames.
    """
    items = []
    with open(filename, newline='') as f:
       reader = csv.DictReader(f)

       for row in reader:
            item = Expando()
            for field in FieldNames:
                setattr(item, field, row[field])

            items.append(item)

    return items
