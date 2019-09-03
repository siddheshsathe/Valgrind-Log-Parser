import os
import json2table

HTML_BUILD_DIRECTION = "LEFT_TO_RIGHT"

html = """
<style>
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

def __get_html_string_formattted(html):
    chars_to_replace = ["</th>", "<table>", "</td>", "</table>"]
    for char in chars_to_replace:
        html = html.replace(char, char + ' \n')
    return html

def dump_html_report(errors_dict={}, html_report_location=None):
    if not html_report_location:
        html_report_location = os.path.join(os.getenv('HOME'), 'valgrind_html_report.html')
    global html
    for log_file_name in errors_dict.keys():
        for error_type in ['memory_leaks', 'syscall_ioctls', 'cond_jump_errors']:
            while('' in errors_dict.get(log_file_name).get(error_type)):
                errors_dict.get(log_file_name).get(error_type).remove('')
    html += json2table.convert(errors_dict, build_direction=HTML_BUILD_DIRECTION)
    html = __get_html_string_formattted(html)
    with open(html_report_location, 'w+') as reportFile:
        reportFile.write(html)
