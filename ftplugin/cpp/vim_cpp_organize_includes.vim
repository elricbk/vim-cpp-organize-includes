" --------------------------------
" Add our plugin to the path
" --------------------------------
python import sys
python import vim
python sys.path.append(vim.eval('expand("<sfile>:h")'))

" --------------------------------
"  Function(s)
" --------------------------------
function! OrganizeCppIncludes()
python << endOfPython
import vim_cpp_organize_includes

vim_cpp_organize_includes.initialize(vim)
start, end, result = vim_cpp_organize_includes.organize_cpp_includes(
    vim.current.buffer
)
if start is None:
    print("No include directives found")
else:
    vim.current.buffer[start:end] = result
    vim.command('redraw')
    print("Includes organized")

endOfPython
endfunction

" --------------------------------
"  Expose our commands to the user
" --------------------------------
command! OrganizeCppIncludes call OrganizeCppIncludes()
