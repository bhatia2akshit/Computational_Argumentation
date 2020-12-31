# CA20 Assignment 3 evaluation script; version 2020-06-19

import argparse
import json
import pandas as pd

from os import path
from sklearn.metrics import f1_score


def evaluate_essays(predictions: list, true_labels: list) -> float:
    """Evaluate the preditions using the f1_score metric. Return the score.

    The order of both input lists does matter and will change the results if different.
    This wrapper uses the weighted F1 score to accomodate an imbalance in labels.

    Arguments:
    predictions -- The list of predicted labels.
    true_labels -- The actual labels of the essays.
    """
    return f1_score(true_labels, predictions)


def main():
    # Read train-test-splits and get test ids
    splits = pd.read_csv(SPLITS_PATH, sep=";")
    test_ids = sorted([int(fn[-3:]) for fn in splits[splits.SET == "TEST"].ID.values])

    #  Read data files from disk
    with open(ESSAYS_PATH, "r") as f:
        data = json.load(f)
    with open(PREDICTIONS_PATH, "r") as f:
        predictions = json.load(f)

    # Extract prediction labels
    # Also, make sure they are sorted based on the integer value of their id
    predictions = sorted(predictions, key=lambda x: int(x["id"]))
    prediction_labels = [1 if e["confirmation_bias"] else 0 for e in predictions]

    # Extract true labels
    # Also, make sure they are sorted based on their id
    y_true = list(filter(lambda x: x["id"] in test_ids, data))
    y_true = sorted(y_true, key=lambda x: x["id"])
    y_true_labels = [1 if e["confirmation_bias"] else 0 for e in y_true]

    # Print the final F1 score to console
    print(f"F1-score: {evaluate_essays(prediction_labels, y_true_labels):.3f}")


if __name__ == "__main__":
    # Parse cli arguments
    SCRIPT_DESCRIPTION = "Simple script to evaluate the essay prediction output"
    parser = argparse.ArgumentParser(description=SCRIPT_DESCRIPTION)
    parser.add_argument(
        "--data_path",
        "-p",
        type=str,
        required=True,
        help="Path to the directory containing the data files.",
        metavar="DATA_PATH")
    args = parser.parse_args()

    # Define all data files paths
    DATA_PATH = args.data_path
    PREDICTIONS_PATH = path.join(DATA_PATH, "predictions.json")
    SPLITS_PATH = path.join(DATA_PATH, "train-test-split.csv")
    ESSAYS_PATH = path.join(DATA_PATH, "essay_corpus.json")

    main()
