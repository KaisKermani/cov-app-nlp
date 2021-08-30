from labeling_check import verify_labels
import spacy
from spacy.tokens import DocBin


def exp_to_docbin(input_path='data/label_studio_out_min.json', output_path='data/labeled.spacy'):
    examples, _, _ = verify_labels(input_path)
    docbin = DocBin()
    for exp in examples:
        docbin.add(exp.y)
    docbin.to_disk(output_path)
    
    
if __name__ == '__main__':
    exp_to_docbin()
