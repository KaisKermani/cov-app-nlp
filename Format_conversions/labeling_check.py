import spacy
import json
from spacy.training import Example
from spacy.language import Language
from customTokenizer import customize_tokenizer
import warnings


def read_labelled(lang: Language, path):
    with open(path, 'rb') as file:
        data = json.load(file)
    
    formatted = []
    ids = []
    for entry in data:
        ents = []
        for ent in entry['label']:
            ents.append([ent['start'], ent['end'], ent['labels'][0]])
        
        cats = {}
        for cat in ['dispo', 'cherche', 'trash']:
            cats[cat] = entry['category'] == cat
        
        formatted.append([
            entry['text'],
            {
                'entities': ents,
                'cats': cats
            }
        ])
        
        ids.append(entry['id'])
            
    examples = []
    bad_labeling = []
    for entry in formatted:
        exp = Example.from_dict(lang.make_doc(entry[0]), entry[1])
        if len(entry[1]['entities']) == len(exp.y.ents):
            examples.append(exp)
        else:
            print("Problem parsing entr:\n\"" + entry[0] + "\"")
            bad_labeling.append(entry)
            pass
    
    return examples, ids, bad_labeling


def verify_labels(path='data/label_studio_out_min.json'):
    warnings.filterwarnings("ignore", category=UserWarning)
    nlp = spacy.blank('fr')
    nlp.tokenizer = customize_tokenizer(nlp)
    return read_labelled(nlp, path)


if __name__ == '__main__':
    verify_labels()
