import re
import os
import json2table
import argparse

from glob import glob
from valgrind_parser.utils.json_helper import JsonHelper
from valgrind_parser.utils.html_converter import dump_html_report
from valgrind_parser.utils.decorators import trycatch
_version = '2.0.3'


class ValgrindLogParser(object):
    """
    This class helps create HTML report out of a valgrind logs
    Arguments:
        valgrind_log_file (str): Relative or absolute path of valgrind logs file to parse
        html_report_location (str): Location of html file to be dumped
    """
    __version__ = _version

    @trycatch
    def __init__(
        self,
        valgrind_log_file,     # Single valgrind log file
        html_report_location=None    # Location of html report to dump
    ):
        self._memleak_regex = None
        self._syscall_ioctl_regex = None
        self._conditional_jump_regex = None
        self._end_regex = None

        self.valgrind_log_file = valgrind_log_file
        if not html_report_location:
            html_report_location = os.getcwd()
        self.html_report_location = html_report_location
        self.regex_json = JsonHelper(os.path.join(os.path.dirname(__file__), 'data', 'valgrind_regexes.json'))
        self.errors_dict = {
            self.valgrind_log_file: {
                "memory_leaks": [],
                "syscall_ioctls": [],
                "cond_jump_errors": []
            }
        }

    @property
    def memleak_regex(self):
        if not self._memleak_regex:
            self._memleak_regex = re.compile(self.regex_json.error_start_regexes.get('memory_leak_start'), re.I)
        return self._memleak_regex

    @property
    def syscall_ioctl_regex(self):
        if not self._syscall_ioctl_regex:
            self._syscall_ioctl_regex = re.compile(self.regex_json.error_start_regexes.get('syscall_errors'), re.I)
        return self._syscall_ioctl_regex

    @property
    def conditional_jump_regex(self):
        if not self._conditional_jump_regex:
            self._conditional_jump_regex = re.compile(
                pattern=self.regex_json.error_start_regexes.get('conditional_jump_errors'),
                flags=re.I
            )
        return self._conditional_jump_regex

    @property
    def end_regex(self):
        if not self._end_regex:
            self._end_regex = re.compile(self.regex_json.error_end_regexes.get('all_error_end_regex'), re.I)
        return self._end_regex

    @trycatch
    def _parser(self):
        with open(self.valgrind_log_file, 'r') as in_file:
            append_lines_flag = False
            leak_trace = ""
            matched_regex = None
            for line in in_file:
                for regex in [self.memleak_regex, self.syscall_ioctl_regex, self.conditional_jump_regex]:
                    start_match = re.match(regex, line.strip('\n'))
                    if start_match:
                        matched_regex = regex
                        append_lines_flag = True

                    end_match = re.match(self.end_regex, line.strip('\n'))
                    if end_match:
                        append_lines_flag = False
                        # Dumping all trace lines to dictionary
                        if not line == '' or line is not None:
                            if matched_regex == self.memleak_regex:
                                self.errors_dict.get(self.valgrind_log_file).get('memory_leaks').append(leak_trace)
                            if matched_regex == self.syscall_ioctl_regex:
                                self.errors_dict.get(self.valgrind_log_file).get('syscall_ioctls').append(leak_trace)
                            if matched_regex == self.conditional_jump_regex:
                                self.errors_dict.get(self.valgrind_log_file).get('cond_jump_errors').append(leak_trace)
                        leak_trace = ''

                    if append_lines_flag:
                        if not line == '' or line is not None:
                            leak_trace += "{line} <br>".format(line=line.strip('\n'))
                        break

    def generate_html_report(self):
        self._parser()
        dump_html_report(self.errors_dict, html_report_location=self.html_report_location)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--valgrind_file',
                        required=True,
                        help="Provide the path of the valgrind file. Files must be of .txt format")

    parser.add_argument('--html_report_location',
                        default='./valgrind_html_report.html',
                        help="Location of HTML report to get dumped at. Default is ./valgrind_html_report.html")

    args = parser.parse_args()
    v = ValgrindLogParser(args.valgrind_file, args.html_report_location)
    v.generate_html_report()
