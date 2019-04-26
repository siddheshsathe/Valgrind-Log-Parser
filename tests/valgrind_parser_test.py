import pytest

class TestValgrindParser(object):
    def setup_class(cls):
        cls.html_report_location = './test_html_report.html'

    def teardown_class(cls):
        import os
        os.remove(cls.html_report_location)

    def test_json_helper(self):
        jsonPath = 'valgrind_parser/valgrind_parser/data/valgrind_regexes.json'
        from valgrind_parser.valgrind_parser.utils.json_helper import JsonHelper
        j = JsonHelper(jsonPath)

    def test_log_parser(self):
        logPath = 'valgrind_parser/test_dir/valgrind_log.txt'
        from valgrind_parser.valgrind_parser.valgrind_log_parser import ValgrindLogParser
        v = ValgrindLogParser(logPath)
        v._parser()

    def test_dump_html_report(self):
        from valgrind_parser.valgrind_parser.utils.html_converter import dump_html_report
        errors_dict = {
            "test": {
                "memory_leaks": [],
                "syscall_ioctls": [],
                "cond_jump_errors": []
            }
        }

        dump_html_report(errors_dict=errors_dict, html_report_location=self.html_report_location)
