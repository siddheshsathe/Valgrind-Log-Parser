import re
import os
import json2table
import argparse

from glob import glob
_version = '0.2.1.0'

import json
class JsonHelper(object):
    def __init__(self, fPath):
        with open(fPath, 'r') as inF:
            self.__dict__ = json.load(inF)

class ValgrindLogParser(object):
    """
    This class helps create HTML report out of a valgrind logs
    Arguments:
        valgrind_log_file (str): Relative or absolute path of valgrind logs file to parse
    """
    __version__ = _version
    def __init__(self,
                valgrind_log_file      # Single valgrind log file
                ):
        self._memleak_regex = None
        self._syscall_ioctl_regex = None
        self._conditional_jump_regex = None
        self._end_regex = None

        self.valgrind_log_file = valgrind_log_file
        self.regex_json = JsonHelper(os.path.join(os.path.dirname(__file__), 'parser_regex.json'))
        self.errors_dict = {
            self.valgrind_log_file:{
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
            self._conditional_jump_regex = re.compile(self.regex_json.error_start_regexes.get('conditional_jump_errors'), re.I)
        return self._conditional_jump_regex

    @property
    def end_regex(self):
        if not self._end_regex:
            self._end_regex = re.compile(self.regex_json.error_end_regexes.get('all_error_end_regex'), re.I)
        return self._end_regex
    
    @property
    def htmlBuildDirection(self):
        return "LEFT_TO_RIGHT"

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
                        if not line == '' or not line == None:
                            if matched_regex == self.memleak_regex:
                                self.errors_dict.get(self.valgrind_log_file).get('memory_leaks').append(leak_trace)
                            if matched_regex == self.syscall_ioctl_regex:
                                self.errors_dict.get(self.valgrind_log_file).get('syscall_ioctls').append(leak_trace)
                            if matched_regex == self.conditional_jump_regex:
                                self.errors_dict.get(self.valgrind_log_file).get('cond_jump_errors').append(leak_trace)
                        leak_trace = ''

                    if append_lines_flag:
                        if not line == '' or not line == None:
                            leak_trace += "{line} <br>".format(line=line.strip('\n'))
                        break

    def generate_html_report(self):
        self._parser()
        print('Removing empty entries')
        for error_type in ['memory_leaks', 'syscall_ioctls', 'cond_jump_errors']:
            while('' in self.errors_dict.get(self.valgrind_log_file).get(error_type)):
                self.errors_dict.get(self.valgrind_log_file).get(error_type).remove('')
        html = """<style>
                    table {
                        color: #333;
                        font-family: Helvetica, Arial, sans-serif;
                        width: 1080px;
                        border-collapse:
                        collapse; border-spacing: 0;
                    }

                    td, th {
                        border: 2px solid; /* No more visible border */
                        height: 30px;
                        transition: all 0.3s;  /* Simple transition for hover effect */
                    }

                    th {
                        background: #45B39D;  /* Darken header a bit */
                        font-weight: bold;
                    }

                    td {
                        background: #FAFAFA;
                        text-align: left;
                    }

                    /* Cells in even rows (2,4,6...) are one color */
                    tr:nth-child(even) td { background: #F1F1F1; }

                    /* Cells in odd rows (1,3,5...) are another (excludes header cells) */
                    tr:nth-child(odd) td { background: #85C1E9; }

                    tr td:hover { background: #666; color: #FFF; }
                    /* Hover cell effect! */
                    </style>
                    """
        html += json2table.convert(self.errors_dict, build_direction=self.htmlBuildDirection)
        with open('valgrind_html_report.html', 'w') as reportFile:
            reportFile.write(html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--valgrind_file', required=True, help="Provide the path of the valgrind file. Files must be of .txt format")

    args = parser.parse_args()
    print('Searching for all files under '.format(args.valgrind_file))
    v = ValgrindLogParser(args.valgrind_file)
    v.generate_html_report()
