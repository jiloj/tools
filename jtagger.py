"""
A utility module for holding jtagger functionality.
"""


import requests


JTAGGER_CREATE_TAGGER_URL = 'http://localhost:9001/taggerrefs/'
JTAGGER_TAG_URL = 'http://localhost:9001/tag'


def create(name, train):
    """
    Create a new tagger given the training data.

    Args:
        name: The name of the new tagger to create.
        train: The training data to use, as a list of clues.

    Returns:
        True if the tagger was succesfully created and False otherwise.
    """
    formatted_train = {}
    for item in train:
        formatted_train[item.id] = item.semanticcategory

    resp = requests.post(JTAGGER_CREATE_TAGGER_URL, json = {
        'name': name,
        'data': formatted_train
    })

    # TODO: What is the point of this line?
    resp.raise_for_status()
    j = resp.json()

    return j['success']


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
