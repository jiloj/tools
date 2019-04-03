"""
A temporary module to hold all of the ml / evaluation type logic.
"""

import itertools

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
        jtagger.create(str(n), train_batch)

        accuracy = evaluate_tagger(tagger, test_batch)
        accuracies.append(accuracy)

        batch_num += 1
        next_start = end

    return accuracies
