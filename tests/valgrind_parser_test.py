import pytest

class TestValgrindParser(object):
    def setup_class(cls):
        cls.html_report_location = './test_html_report.html'
        cls.log_path = './test_dir/valgrind_log.txt'
        cls.json_path = './valgrind_parser/data/valgrind_regexes.json'

    def teardown_class(cls):
        import os
        os.remove(cls.html_report_location)

    def test_json_helper(self):
        from valgrind_parser.utils.json_helper import JsonHelper
        j = JsonHelper(self.json_path)

    def test_log_parser(self):
        from valgrind_parser.valgrind_log_parser import ValgrindLogParser
        v = ValgrindLogParser(self.log_path)
        v._parser()

    def test_dump_html_report(self):
        from valgrind_parser.utils.html_converter import dump_html_report
        errors_dict = {
            "test": {
                "memory_leaks": [],
                "syscall_ioctls": [],
                "cond_jump_errors": []
            }
        }

        dump_html_report(errors_dict=errors_dict, html_report_location=self.html_report_location)

    def test_report_generation_wrapper(self):
        from valgrind_parser import generate_valgrind_report
        generate_valgrind_report(self.log_path, html_report_location='./valgrind_html_report.html')
