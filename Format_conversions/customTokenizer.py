import spacy
from spacy.lang.char_classes import ALPHA
from spacy.tokenizer import Tokenizer


def customize_tokenizer(lang):

    prefixes = lang.Defaults.prefixes
    suffixes = lang.Defaults.suffixes

    chars = ['<', '>', '=', '_', '-', '|']
    for c in chars:
        try:
            prefixes.remove(c)
        except ValueError:
            pass
        try:
            suffixes.remove(c)
        except ValueError:
            pass

    prefixes = prefixes + [r'''^[_~\-><|=:/]+''', ]  # Special characters
    prefixes = prefixes + [r'''^[0-9]+(?=[a-z])''', ]   # Dividing numbers and alphas
    suffixes = suffixes + [r'''[_~\-><|=:/]+$''', ]  # Special chars
    suffixes = suffixes + [r'''(?<=[a-z])[0-9]+$''', ]  # Dividing numbers and alphas

    suffix_re = spacy.util.compile_suffix_regex(suffixes)
    # lang.tokenizer.suffix_search = suffix_re.search

    prefix_re = spacy.util.compile_prefix_regex(prefixes)
    # lang.tokenizer.prefix_search = prefix_re.search

    # infixes = lang.Defaults.infixes + [r"(?<=[{a}0-9])(?:[\(\)_~\-><|=:/]+)(?=[{a}0-9])".format(a=ALPHA), ]
    infixes = lang.Defaults.infixes + [r"(?:[\(\)_~\-><|=:/]+)".format(a=ALPHA), ]
    infixes = infixes + [r"(?<=[{a}])(?:[0-9]+)(?=[{a}])".format(a=ALPHA), ]
    infix_re = spacy.util.compile_infix_regex(infixes)
    # lang.tokenizer.infix_finditer = infix_re.finditer

    # Special Cases:
    rules = lang.tokenizer.rules
    rules.pop('h.')

    return Tokenizer(
        lang.vocab, rules=rules, prefix_search=prefix_re.search,
        suffix_search=suffix_re.search, infix_finditer=infix_re.finditer
    )
