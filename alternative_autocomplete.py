from contextlib import contextmanager
from os.path import join
import imp
import os
import re
import sublime
import sublime_plugin
#TODO: add caching mechanizm
#last modified: 23.9.2011 by ask


class AlternativeAutocompleteCommand(sublime_plugin.TextCommand):

    candidates = []
    previous_completion = None

    def run(self, edit):

        self.edit = edit
        self.show_panel(self.on_choise_insert)

    def suggestions(self, position, text):
        prefix_match = re.search(r'([\w\d_]+)\Z', text[0:position], re.M | re.U)
        if prefix_match:
            prefix = prefix_match.group(1)
        self.p = prefix_match
        candidates = []
        load_sources()
        for source in g_sources:
            candidates.append(source['completion'](self.view, prefix, position, text))
            # print(source['name'])
            # print(source['completion'](self.view, prefix, position, text))
        global g_sources
        g_sources = []
        return flatten(candidates)

    def show_panel(self, callback):
        self.suggestions_list = self.suggestions(self.view.sel()[0].b,
            self.view.substr(sublime.Region(0, self.view.size())))
        self.view.window().show_quick_panel(self.suggestions_list, callback)

    def on_choise_insert(self, choise):
        if choise == -1:
            return
        with edit(self.view) as e:
            choise = self.suggestions_list[choise]
            self.view.replace(e, sublime.Region(self.p.start(1), self.p.end(1)), choise)


g_sources = []


def define_source(source_or_func):
    """Define completion source"""
    if callable(source_or_func):
        source = {'name': source_or_func.__name__, 'completion': source_or_func}
    # if source['name'] not in [x['name'] for x in g_sources]:
    g_sources.append(source)


def is_python_file(file_name):
    """Helper for filtering snippet files"""
    return file_name.endswith(".py")


def load_sources():
    sources_path = join(sublime.packages_path(), 'alternative_autocompletion/sources')
    sources = os.listdir(sources_path)
    for source_dir in sources:
        fm = imp.find_module('completions', [join(sources_path, source_dir)])
        imp.load_module('', *fm)


@contextmanager
def edit(view):
    """Context manager start and finish undo stage"""
    edit_sequence = view.begin_edit()
    yield edit_sequence
    view.end_edit(edit_sequence)

flatten = lambda l: [item for sublist in l for item in sublist]
