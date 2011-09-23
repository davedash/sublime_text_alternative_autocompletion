maybe_split = lambda s: s.split() if len(s) > 1 else s
strip = lambda s: s.strip()
maybe_flatten = lambda l: [item if not isinstance(item, list) else sublist for sublist in l for item in sublist]
both = lambda f, g: lambda x, f=f, g=g: f(g(x))


def translate_non_alphanumerics(to_translate, translate_to=u''):
    not_letters_or_digits = u'!"$#%\'()*+,./:;<=>?@[\]^`{|}~'
    translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)
    return to_translate.translate(translate_table)


def normalize(words):
    cleaned = [translate_non_alphanumerics(word) for word in words]
    return maybe_flatten(map(both(maybe_split, strip), cleaned))
