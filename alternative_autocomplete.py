import sublime
import sublime_plugin
import re
from contextlib import contextmanager

#TODO: add caching mechanizm
#Add unite all completion functionality
#last modified: 22.9.2011 by ask


@contextmanager
def edit(view):
    """Context manager start and finish undo stage"""
    edit_sequence = view.begin_edit()
    yield edit_sequence
    view.end_edit(edit_sequence)


def uniq(list):
    seen = set()
    return [value for value in list if value not in seen and not seen.add(value)]


def fuzzy_match(query, word):
    query, word = query.lower(), word.lower()
    qi, wi = 0, 0
    while qi < len(query):
        wi = word.find(query[qi], wi)
        if wi == -1:
            return False
        qi += 1
    return True


class Candidate:
    def __init__(self, distance, text):
        self.distance = distance
        self.text = text

    def __hash__(self):
        return hash(self.text)

    def __cmp__(self, other):
        return cmp(self.text, other.text)


class AlternativeAutocompleteCommand(sublime_plugin.TextCommand):

    candidates = []
    previous_completion = None

    def run(self, edit, cycle='next', default=''):

        self.edit = edit
        self.show_panel(self.on_choise_insert)

    def suggestions(self, position, text, text_currentbuffer):
        prefix_match = re.search(r'([\w\d_]+)\Z', text_currentbuffer[0:position], re.M | re.U)
        if prefix_match:
            prefix = prefix_match.group(1)
        self.p = prefix_match
        candidates = self.find_candidates(prefix, position, text)
        return candidates

    def show_panel(self, callback):
    	textfor = lambda view: view.substr(sublime.Region(0, view.size()))
    	# for some reason
    	# "textfor(v) for v in w.views() for w in sublime.windows()" doesn't
    	text = ''
    	for w in sublime.windows():
    		for v in w.views():
    			text += textfor(v)
        self.suggestions_list = self.suggestions(
        	self.view.sel()[0].b,
        	text,
        	self.view.substr(sublime.Region(0, self.view.size())))
        self.view.window().show_quick_panel(self.suggestions_list, callback)

    def on_choise_insert(self, choise):
        if choise == -1:
            return
        with edit(self.view) as e:
            choise = self.suggestions_list[choise]
            self.view.replace(e, sublime.Region(self.p.start(1), self.p.end(1)), choise)

    def find_candidates(self, prefix, position, text):
        candidates = []
        regex = re.compile(r'[^\w\d](' + re.escape(prefix) + r'[\w\d]+)', re.M | re.U)
        for match in regex.finditer(text):
            candidates.append(Candidate(abs(match.start(1) - position), match.group(1)))
            if len(candidates) > 100:
                break
        if candidates:
            candidates.sort(lambda a, b: cmp(a.distance, b.distance))
            candidates = [candidate.text for candidate in candidates]
        else:
            word_regex = re.compile(r'\b' + re.escape(prefix[0:1]) + r'[\w\d]+', re.M | re.U | re.I)
            words = word_regex.findall(text)
            candidates = [word for word in words if word != prefix and fuzzy_match(prefix, word)]
        if candidates:
            candidates.append(prefix)
        return uniq(candidates)
