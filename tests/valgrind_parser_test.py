import os
from valgrind_parser.valgrind_parser.utils.html_converter import dump_html_report
from valgrind_parser import generate_valgrind_report
from valgrind_parser.valgrind_parser.utils.json_helper import JsonHelper
from valgrind_parser.valgrind_parser.valgrind_log_parser import ValgrindLogParser
from valgrind_parser.valgrind_parser.utils.decorators import trycatch
from valgrind_parser.valgrind_parser.utils.decorators import singleton
import pytest

class TestValgrindParser(object):
    def setup_class(cls):
        cls.html_report_location = './test_html_report.html'

    def teardown_class(cls):
        if os.path.exists(cls.html_report_location):
            os.remove(cls.html_report_location)

    def test_json_helper(self):
        jsonPath = 'valgrind_parser/valgrind_parser/data/valgrind_regexes.json'
        j = JsonHelper(jsonPath)

    def test_log_parser(self):
        logPath = 'valgrind_parser/test_dir/valgrind_log.txt'
        v = ValgrindLogParser(logPath)
        v._parser()

    def test_dump_html_report(self):
        errors_dict = {
            "test": {
                "memory_leaks": [],
                "syscall_ioctls": [],
                "cond_jump_errors": []
            }
        }

        dump_html_report(errors_dict=errors_dict, html_report_location=self.html_report_location)

    def test_generate_valgrind_report_function(self):
        logPath = 'valgrind_parser/test_dir/valgrind_log.txt'
        generate_valgrind_report(logPath)

    def test_decorator_trycatch(self):
        @trycatch
        def internal_test_function():
            raise Exception

        internal_test_function()

    def test_decorator_singleton(self):
        @singleton
        class TestClass:
            pass

        object1 = TestClass()
        object2 = TestClass()

        assert object1 is object2, "Test class objects are different"
