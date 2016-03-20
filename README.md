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

The only available option is `g:organize_includes_company_prefix` which lets you
to set your company prefix for moving corresponding includes to separate group.

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

* Tests
* Support for optional lines between groups
* Support for includes with comments
