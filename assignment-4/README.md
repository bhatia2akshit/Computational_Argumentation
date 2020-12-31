# Computational Argumentation 2020 - Assignment 4

## Task
- The task is to develop a text generation approach to generate the prompt of an argumentative essay.

## Data: 

- We provide a dataset of 402 essays with their prompts (Stab and Gurevych. 2016. Parsing Argumentation Structure in Persuasive Essays).

- If you think your approach might need more data, then feel free to use any external dataset that you think might help you in this task!

- Hint: for this task, we ask you not to use the ground truth annotations given in previous assignments, such as major-claims, claims, and premises, but rather, in case you need such annotations, use your argument mining approach you developed early in the previous assignment.


### How to use the evaluation script?

- For evaluation, we are using the ROUGE score.
	- To be able to run the evaluation, you have to install the rouge library:
		```shell
			$ pip install rouge==1.0.0
			$ pip install pandas==0.23.4
		```

You can run the evaluation script on the predictions data using the following command:
```shell
# Assuming you are in the code directory
$ python evaluation --data_path ../data
```

The script assumes that the data directory contains the predictions in the given format (see `data/sample_prediction.json`) and the unified data file. It will print a simple score to the console.
