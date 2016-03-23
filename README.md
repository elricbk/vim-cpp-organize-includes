# vim-cpp-organize-includes

## What it does

Sorts, uniqs and groups include directive in C++ files. Will transform this:

    #include <string>
    #include <vector>
    #include "local1.h"
    #include <boost/optional.hpp>
    #include "local1.h"
    #include "local2.h"
    #include <yourcomany/file1.h>
    #include <yourcomany/file2.h>

To this:

    #include "local1.h"
    #include "local2.h"

    #include <yourcomany/file1.h>
    #include <yourcomany/file2.h>

    #include <boost/optional.hpp>
    #include <string>
    #include <vector>

Plugin adds command `OrganizeCppIncludes` which performs the transformation.

Available options:
* `g:organize_includes_company_prefix` lets you to set your company prefix for
moving corresponding includes to separate group
* `g:organize_includes_lines_between_groups` allows you to disable adding empty
lines between groups if set to `0` (default value is `1`).

## Requirements

`python` support for Vim.

## Installation

Use your plugin manager of choice.

- [Pathogen](https://github.com/tpope/vim-pathogen)
  - `git clone https://github.com/elricbk/vim-cpp-organize-includes ~/.vim/bundle/vim-cpp-organize-includes`
- [Vundle](https://github.com/gmarik/vundle)
  - Add `Bundle 'elricbk/vim-cpp-organize-includes'` to .vimrc
  - Run `:BundleInstall`
- [NeoBundle](https://github.com/Shougo/neobundle.vim)
  - Add `NeoBundle 'elricbk/vim-cpp-organize-includes'` to .vimrc
  - Run `:NeoBundleInstall`
- [vim-plug](https://github.com/junegunn/vim-plug)
  - Add `Plug 'elricbk/vim-cpp-organize-includes'` to .vimrc
  - Run `:PlugInstall`

## Todo

* More tests
* Correct support for "company" includes (not just `.find(prefix)`)
* Support for includes with excessive spaces
* Support for includes with comments
* Docs
