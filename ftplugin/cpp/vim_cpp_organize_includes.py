import itertools
import os

COMPANY_PREFIX_KEY = 'g:organize_includes_company_prefix'
LINES_BETWEEN_GROUPS_KEY = 'g:organize_includes_lines_between_groups'
INCLUDE_MARKER = '#include'

vim = None

def _get_global_variable(key):
    eval_value = int(vim.eval('exists("%s")' % key))
    if not eval_value: return None
    return vim.eval(key)

def find_include_range(buf):
    start = None
    end = None
    is_empty = lambda s: len(s.strip()) == 0
    is_include = lambda s: s.strip().startswith(INCLUDE_MARKER)
    for i, l in enumerate(buf):
        if is_empty(l): continue
        if start is None and is_include(l):
            start = i
        if not is_include(l) and start is not None:
            end = i
            break
    if start is not None and end is None:
        end = i + 1
    while end > start and len(buf[end - 1].strip()) == 0:
        end -= 1
    return (start, end)

def _non_empty(l):
    return len(l.strip()) != 0

def _is_local(l):
    return l.find('"') != -1

def _is_global(l):
    return l.find('<') != -1

def _include_path(l):
    l = l.replace(INCLUDE_MARKER, '').strip()
    if len(l) < 2: return None
    return l[1:-1]

def _is_company(l, company_prefix):
    if company_prefix is None: return False
    p = _include_path(l)
    if p is None: return False
    prefix = p.split('\\')[0].split('/')[0]
    return prefix == company_prefix

def _filename(name):
    base_name = os.path.basename(name)
    return os.path.splitext(base_name)[0]

def _same_basename(l, buffer_base_name):
    p = _include_path(l)
    if p is None: return False
    return _filename(p) == buffer_base_name

def _remove_whitespace(l):
    l = l.strip()
    assert l.startswith(INCLUDE_MARKER)
    l = l.replace(INCLUDE_MARKER, '')
    return INCLUDE_MARKER + ' ' + l.strip()

class IncludeType:
    THIS_FILE_HEADER = 0
    LOCAL = 1
    COMPANY = 2
    GLOBAL = 3

def get_include_type(l, company_prefix, buffer_name):
    if _same_basename(l, buffer_name): return IncludeType.THIS_FILE_HEADER
    if _is_company(l, company_prefix): return IncludeType.COMPANY
    if _is_global(l): return IncludeType.GLOBAL
    return IncludeType.LOCAL

def organize_cpp_includes(b):
    start, end = find_include_range(b)
    if start is None: return (start, end, None)

    _get_include_type = lambda l: get_include_type(
        l,
        _get_global_variable(COMPANY_PREFIX_KEY),
        _filename(vim.current.buffer.name)
    )

    include_list = itertools.groupby(
        sorted(
            set(map(_remove_whitespace, filter(_non_empty, b[start:end]))),
            key=lambda l: (_get_include_type(l), l)
        ),
        lambda l: _get_include_type(l)
    )

    add_lines = _get_global_variable(LINES_BETWEEN_GROUPS_KEY)
    if add_lines is not None:
        add_lines = (add_lines == "1")
    else:
        add_lines = True

    result = []
    for _, g in include_list:
        result.extend(g)
        if add_lines:
            result.append('')
    if len(result) > 0: result.pop()

    return (start, end, result)

def initialize(vim_ext):
    global vim
    vim = vim_ext
