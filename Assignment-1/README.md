### TASK

Download corpora:
	- Argument Annotated Essays (version 2) : https://www.informatik.tu-darmstadt.de/ukp/research_6/data/argumentation_mining_1/argument_annotated_essays_version_2/index.en.jsp
	- Insufficiently Supported Arguments in Argumentative Essays: https://www.informatik.tu-darmstadt.de/ukp/research_6/data/argumentation_mining_1/insufficiently_supported_arguments/index.en.jsp
	- Opposing Arguments in Persuasive Essays: https://www.informatik.tu-darmstadt.de/ukp/research_6/data/argumentation_mining_1/opposing_arguments_in_persuasive_essays/index.en.jsp


Corpora Unification: Each object represents an essay that contains:
	- Essay Identifier
	- Essay text
	- Confirmation bias as a boolean label
	- List of Paragraphs; each as a json object containing text, and the sufficient label
	- Premises, Claims and Major Claims each as a list of json objects, where each object contains text and span as tuple.

Preliminary Statistics: On the training split perform the following:
	- Number of essays, paragraphs, sentences, and tokens (use spaCy api for
	tokenization).
	- Number of major claims, claims, premises.
	- Number of essays with and without confirmation bias.
	- Number of sufficient and insufficient paragraphs (arguments).
	- Average number of tokens in major claims, claims, and premises.
	- The 10 most specific words in major claims, claims, and premises.