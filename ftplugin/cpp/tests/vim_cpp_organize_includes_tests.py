import unittest
import vim_cpp_organize_includes as sut
import mock


class GetIncludeTypeTest(unittest.TestCase):
    def test_given_local_file_returns_local(self):
        result = sut.get_include_type('#include "test.h"', 'company', '')
        self.assertEqual(sut.IncludeType.LOCAL, result)

    def test_given_global_file_returns_global_type(self):
        result = sut.get_include_type('#include <string>', 'company', '')
        self.assertEqual(sut.IncludeType.GLOBAL, result)

    def test_given_local_company_file_returns_company(self):
        result = sut.get_include_type('#include "company/f.hpp"', 'company', '')
        self.assertEqual(sut.IncludeType.COMPANY, result)

    def test_given_company_prefix_not_at_start_doesnt_return_company(self):
        result = sut.get_include_type('#include "nottest/f.hpp"', 'test', '')
        self.assertNotEqual(sut.IncludeType.COMPANY, result)

    def test_given_global_company_file_returns_company(self):
        result = sut.get_include_type('#include <company/f.hpp>', 'company', '')
        self.assertEqual(sut.IncludeType.COMPANY, result)

    def test_given_header_for_cpp_file_returns_this_file_header(self):
        result = sut.get_include_type('#include "test.h"', 'company', 'test')
        self.assertEqual(sut.IncludeType.THIS_FILE_HEADER, result)

class FindIncludeRangeTest(unittest.TestCase):
    def test_for_basic_case_returns_expected_result(self):
        buf = ['#include <string>']

        start, end = sut.find_include_range(buf)

        self.assertEqual(start, 0)
        self.assertEqual(end, 1)

    def test_for_includes_not_from_first_line_returns_expected_result(self):
        buf = ['', '#include <string>', '#include <vector>']

        start, end = sut.find_include_range(buf)

        self.assertEqual(start, 1)
        self.assertEqual(end, 3)

    def test_given_trailing_empty_lines_doesnt_treat_them_as_includes(self):
        buf = ['', '#include <string>', '', '']

        start, end = sut.find_include_range(buf)

        self.assertEqual(start, 1)
        self.assertEqual(end, 2)

    def test_given_empty_lines_between_directives_includes_them_in_result(self):
        buf = ['', '#include <string>', '', '#include <vector>']

        start, end = sut.find_include_range(buf)

        self.assertEqual(start, 1)
        self.assertEqual(end, 4)

    def test_given_no_includes_in_file_returns_none(self):
        buf = ['', '<string>', '', '<vector>']

        start, end = sut.find_include_range(buf)

        self.assertIsNone(start)
        self.assertIsNone(end)

class OrganizeCppIncludesTest(unittest.TestCase):
    def setUp(self):
        mock_vim = mock.Mock()
        mock_vim.eval = mock.Mock(return_value=0)
        mock_vim.current.buffer.name = ''
        sut.initialize(mock_vim)

    def test_given_buffer_with_no_includes_returns_none(self):
        buf = ['', 'test', 'me', '']

        start, _, _ = sut.organize_cpp_includes(buf)

        self.assertIsNone(start)

    def test_given_buffer_with_includes_organizes_them(self):
        buf = [
            '#include <vector>',
            '#include "local.h"',
            '#include <string>',
        ]

        _, _, result = sut.organize_cpp_includes(buf)

        self.assertEqual(result, [
            '#include "local.h"',
            '',
            '#include <string>',
            '#include <vector>',
        ])

    def test_given_repeated_includes_leaves_only_one(self):
        buf = [
            '#include <vector>',
            '#include <vector>',
            '#include "string"',
            '#include "string"',
        ]

        _, _, result = sut.organize_cpp_includes(buf)

        self.assertEqual(result, [
            '#include "string"',
            '',
            '#include <vector>',
        ])

    def test_given_repeated_includes_with_spaces_leaves_only_one(self):
        buf = [
            '#include   <vector>',
            '#include <vector>  ',
        ]

        _, _, result = sut.organize_cpp_includes(buf)

        self.assertEqual(result, [
            '#include <vector>',
        ])
