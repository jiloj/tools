"""
A temporary module to hold all of the ml / evaluation type logic.
"""

import csv
import itertools
import os
import time

import data
import jtagger


def evaluate_tagger(tagger, dataset):
    """
    Evaluates a specific tagger instance against the given dataset.

    Args:
        tagger: The name of the tagger instance to evaluate.
        dataset: The labeled dataset to use as evaluation.

    Returns:
        The accuracy of the tagger on the dataset as a floating point number.
    """
    correct = 0

    for item in dataset:
        r = int(item.round)
        v = int(item.value)
        guess = jtagger.tag(tagger, item.category, item.question, item.answer, r, v)
        actual = item.semanticcategory

        correct += int(actual.lower() == guess.lower())

    return correct / len(dataset)


def cross_validate(dataset, n):
    """
    Run cross validation on the tagger model with n batches.

    Args:
        dataset: The entire dataset to use for the cross validation computation.
        n: The number of batches to run the cross validation through.

    Returns:
        The accuracy for each of the batches during cross validation.
    """
    run_id = int(time.time())

    accuracies = []

    total = len(dataset)
    batch_size = total / n

    # TODO: This is generally right, but I need to make sure rounding errors
    #       and some edge cases still work.
    # TODO: Is there a nicer way to do this?
    next_start = 0
    batch_num = 1
    while next_start < total:
        start = next_start
        end = int(batch_num * batch_size + 0.5)

        # TODO: note slice copy
        # TODO: make immutable
        test_batch = dataset[start:end]
        train_batch = dataset[:start] + dataset[end:]
        train_filename = '{}-{}.csv'.format(run_id, batch_num)

        abs_path = ''
        with open(train_filename, 'w', newline='') as f:
            abs_path = os.path.abspath(f.name)
            writer = csv.DictWriter(f, data.FieldNames)
            writer.writeheader()
            for row in train_batch:
                writer.writerow(row.__dict__)

        tagger_instance_name = '{}-{}'.format(run_id, batch_num)
        success, task_id = jtagger.create(tagger_instance_name, abs_path)
        print('Creating tagger {}'.format(tagger_instance_name))

        # Wait until the tagger completes.
        tagger_complete = False
        while not tagger_complete:
            _, tagger_complete = jtagger.task_status(task_id)
            print('Waiting 5 seconds for {}'.format(tagger_instance_name))
            time.sleep(5)

        accuracy = evaluate_tagger(tagger_instance_name, test_batch)
        print('{} accuracy for batch #{}'.format(accuracy, batch_num))
        accuracies.append(accuracy)

        batch_num += 1
        next_start = end

    return accuracies
