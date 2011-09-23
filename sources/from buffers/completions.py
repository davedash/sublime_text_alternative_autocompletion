from alternative_autocomplete import define_source
from matchers import fuzzy
from filters import normalize
import sublime


@define_source
def from_all_opened_buffers(view, prefix, position, text):
    windows = sublime.windows()
    views = [v.views() for v in windows]
    texts = [v.substr(sublime.Region(0, v.size())) for w in views for v in w]
    words = [normalize.normalize(w.split()) for w in texts]
    possibilities = filter(filter_none, [uniq(text) for text in words])
    candidates = [fuzzy.match(prefix, posib) for posib in possibilities]
    print(possibilities)
    return sorted([item[0] for sublist in sorted(candidates) for item in sublist])


filter_none = lambda l: filter(None, l)


def uniq(list):
    seen = set()
    return [value for value in list if value not in seen and not seen.add(value)]
