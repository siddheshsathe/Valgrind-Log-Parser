import os
import logging
from valgrind_parser.valgrind_log_parser import ValgrindLogParser
from valgrind_parser.utils.decorators import trycatch

@trycatch
def generate_valgrind_report(valgrind_log_file, html_report_location='./valgrind_html_report.html'):
    """
    Function to generate valgrind report after parsing the valgrind logs.
    Args:
        valgrind_log_file (str): Path for the valgrind file.
        html_report_location (str): Path for html report
    """
    try:
        assert os.path.exists(valgrind_log_file), "Valgrind log file doesn't exist at given path"
        v = ValgrindLogParser(valgrind_log_file, html_report_location)
        v.generate_html_report()
    except Exception as e:
        logging.exception(e)
    finally:
        del v  # Deleting the object of the class
