import unittest
import vim_cpp_organize_includes as sut


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
        self.assertEqual(end, 0)

    def test_for_includes_not_from_first_line_returns_expected_result(self):
        buf = ['', '#include <string>', '#include <vector>']

        start, end = sut.find_include_range(buf)

        self.assertEqual(start, 1)
        self.assertEqual(end, 2)

    def test_given_trailing_empty_lines_treats_them_as_include_lines(self):
        buf = ['', '#include <string>', '', '']

        start, end = sut.find_include_range(buf)

        self.assertEqual(start, 1)
        self.assertEqual(end, 3)

    def test_given_empty_lines_between_directives_includes_them_in_result(self):
        buf = ['', '#include <string>', '', '#include <vector>']

        start, end = sut.find_include_range(buf)

        self.assertEqual(start, 1)
        self.assertEqual(end, 3)

    def test_given_no_includes_in_file_returns_none(self):
        buf = ['', '<string>', '', '<vector>']

        start, end = sut.find_include_range(buf)

        self.assertIsNone(start)
        self.assertIsNone(end)

