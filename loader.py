from os.path import join
import sublime
import sys

lib = join(sublime.packages_path(), 'alternative_autocompletion')
if lib not in sys.path:
    sys.path.append(lib)
