import vim
import itertools
import os

COMPANY_PREFIX_KEY = "g:organize_includes_company_prefix"

def _get_global_variable(key):
    eval_value = int(vim.eval('exists("%s")' % key))
    if not eval_value: return None
    return vim.eval(key)

def _find_include_range(buf):
    start = None
    end = None
    is_empty = lambda s: len(s.strip()) == 0
    is_include = lambda s: s.strip().startswith('#include')
    for i, l in enumerate(buf):
        if is_empty(l): continue
        if start is None and is_include(l):
            start = i
        if not is_include(l) and start is not None:
            end = i - 1
            break
    if start is not None and end is None:
        end = i
    return (start, end)

def _non_empty(l):
    return len(l.strip()) != 0

def _is_local(l):
    return l.find('"') != -1

def _is_global(l):
    return l.find('<') != -1

def _is_company(l, company_prefix):
    if company_prefix is None: return False
    return l.find(company_prefix) != -1

def _filename(name):
    base_name = os.path.basename(name)
    return os.path.splitext(base_name)[0]

def _same_basename(l, buffer_base_name):
    l = l.replace('#include', '').strip()
    if len(l) < 2: return False
    return _filename(l[1:-1]) == buffer_base_name

class IncludeType:
    THIS_FILE_HEADER = 0
    LOCAL = 1
    COMPANY = 2
    GLOBAL = 3

def _get_include_type(l, company_prefix, buffer_name):
    if _same_basename(l, buffer_name): return IncludeType.THIS_FILE_HEADER
    if _is_company(l, company_prefix): return IncludeType.COMPANY
    if _is_global(l): return IncludeType.GLOBAL
    return IncludeType.LOCAL

def organize_cpp_includes():
    b = vim.current.buffer
    start, end = _find_include_range(b)
    if start is None:
        print "No include directives found"
        return
    
    get_include_type = lambda l: _get_include_type(
        l,
        _get_global_variable(COMPANY_PREFIX_KEY),
        _filename(vim.current.buffer.name)
    )
    
    include_list = itertools.groupby(
        sorted(
            set(filter(_non_empty, b[start:end])),
            key=lambda l: (get_include_type(l), l)
        ),
        lambda l: get_include_type(l)
    )
    result = []
    for _, g in include_list:
        result.extend(g)
        result.append('')
    if len(result) > 0: result.pop()
    b[start:end] = result
    vim.command('redraw')
    print "Includes organized"
