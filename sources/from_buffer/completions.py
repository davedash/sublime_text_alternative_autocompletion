from alternative_autocomplete import define_source
from matchers import fuzzy
import sublime
import re


@define_source
def from_all_opened_buffers(view, prefix, position, text):
    windows = sublime.windows()
    views = [v.views() for v in windows]
    texts = [v.substr(sublime.Region(0, v.size())) for w in views for v in w]
    word_regex = re.compile(r'\b' + re.escape(prefix[0:1]) + r'[\w\d]+', re.M | re.U | re.I)
    words = [word_regex.findall(text) for text in texts]
    possibilities = filter(filter_none, [uniq(text) for text in words])
    candidates = [fuzzy.match(prefix, posib) for posib in possibilities]
    return sorted([item[0] for sublist in sorted(candidates) for item in sublist])

filter_none = lambda l: filter(None, l)


def uniq(list):
    seen = set()
    return [value for value in list if value not in seen and not seen.add(value)]
