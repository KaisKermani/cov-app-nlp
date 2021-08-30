import json
from spacy.training import Example
from spacy.language import Language


def load_examples(lang: Language, path='../Data/all_labeled.json'):
	with open(path, 'r') as file:
		data = json.load(file)
	
	examples = []
	for entry in data.values():
		try:
			examples.append(Example.from_dict(lang.make_doc(entry[0]), entry[1]))
		except ValueError:
			print(entry[0])
			pass
	return examples, list(data.keys())
