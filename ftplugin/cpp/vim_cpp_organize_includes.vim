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

from vim_cpp_organize_includes import organize_cpp_includes
organize_cpp_includes()

endOfPython
endfunction

" --------------------------------
"  Expose our commands to the user
" --------------------------------
command! OrganizeCppIncludes call OrganizeCppIncludes()
