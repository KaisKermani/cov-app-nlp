import spacy
from customTokenizer import customize_tokenizer
from loadExamples import load_examples
import json


def doc_ser(doc):
    results = []
    for ent in doc.ents:
        results.append({
            'from_name': 'label',
            'to_name': 'text',
            'type': 'labels',
            'value': {
                'start': ent.start_char,
                'end': ent.end_char,
                'text': ent.text,
                'labels': [ent.label_]
            }
        })
    
    cat = [k for k, v in doc.cats.items() if v]
    results.append({
        "from_name": "category",
        "to_name": "text",
        "type": "choices",
        "value": {
            "choices": cat
        }
    })

    ser = {
        'data': {'text': doc.text},
        'predictions': [{'model_version': 'NLP', 'result': results}]
    }
    
    return ser


def docs_to_ls():
    nlp = spacy.blank('fr')
    nlp.tokenizer = customize_tokenizer(nlp)
    
    examples, keys = load_examples(nlp, 'data/spacy v2.json')
    
    tasks = []
    for exp in examples:
        tasks.append(doc_ser(exp.y))
    
    print("Done")

    with open('data/label_studio_tasks.json', mode='w') as f:
        json.dump(tasks, f, indent=2)


if __name__ == '__main__':
    docs_to_ls()
