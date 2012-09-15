from pygments.lexers import get_all_lexers, get_lexer_by_name, guess_lexer
from pygments.styles import get_all_styles
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
from pygments import highlight

LEXER_LIST_ALL = sorted([(i[1][0], i[0]) for i in get_all_lexers()])
LEXER_LIST = (
    ('bash', 'bash'),
    ('c', 'C'),
    ('c++', 'C++'),
    ('diff', 'patch or diff'),
    ('java', 'Java'),
    ('matlab', 'MATLAB'),
    ('octave', 'Octave'),
    ('perl', 'Perl'),
    ('php', 'PHP'),
    ('python', 'Python'),
    ('text', 'Text only'),
)
LEXER_DEFAULT = 'octave'


class NakedHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile):
        return self._wrap_code(source)
    def _wrap_code(self, source):
        for i, t in source:
            yield i, t

def pygmentize(code_string, lexer_name='text'):
    return highlight(code_string, get_lexer_by_name(lexer_name),
                     NakedHtmlFormatter())

def guess_code_lexer(code_string, default_lexer='unknown'):
    try:
        return guess_lexer(code_string).name
    except ClassNotFound:
        return default_lexer
