# Computational Argumentation 2020 - Assignment 3

## Task
Your main task is to develop an approach that allows you to predict the quality of arguments in an essay, as measured by the _confirmation bias_ dimension. Like in the last assignments, please document your choice properly and justify the selection of features and models. Especially the feature selection and justification will make a big contribution towards your grade. So please don't just use the latest word embeddings (even though they might be part of the feature vectors, if justified properly), but also consider other properties of the text that help with assessing the quality of arguments.

## Evaluation
When reviewing your submissions, we will try to reproduce the results you submitted alongside your code. For this, we will use the evaluation script `code/conf_bias_evaluation.py`. So please make sure that the output of your code matches the expected predictions format. You can find a sample in `data/sample_prediction.json`.

### How to use the evaluation script?
You can run the evaluation script on the predictions data using the following command:
```shell
# Assuming you are in the code directory
$ python conf_bias_evaluation --data_path ../data
```

The script assumes that the data directory contains the predictions in the given format (see `data/sample_prediction.json`) and the unified data file. It will print a simple score to the console.
