import os
from valgrind_parser.valgrind_log_parser import ValgrindLogParser

def generate_valgrind_report(valgrind_log_file_path, html_report_location='./valgrind_html_report.html'):
    """
    Wrapper to generate the valgrind html report
    Args:
        valgrind_log_file_path (str): Path of valgrind log file
        html_report_location (str): Location of generated valgrind html report

    Raises:
        AssertionError: If valgrind_log_file_path doesn't exist
    """
    assert os.path.exists(valgrind_log_file_path), "Valgrind log file path doesn't exist"
    if not html_report_location.endswith('.html'):
        os.path.join(html_report_location, 'valgrind_html_report.html')
    v = ValgrindLogParser(valgrind_log_file_path, html_report_location)
    v.generate_html_report()
