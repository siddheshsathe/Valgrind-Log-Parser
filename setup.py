from setuptools import setup, find_packages
from valgrind_parser.valgrind_log_parser import _version

import os
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
    long_description = f.read()

setup(name='valgrind_parser',
      version=_version,
      description='The valgrind logs parser. Creates the html report from txt logs.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/siddheshsathe/Valgrind-Log-Parser',
      author='Siddhesh Sathe',
      author_email='siddheshsathe@rediffmail.com',
      licence='GNU General Public License v3.0',
      packages=find_packages(),
      package_dir={'valgrind_parser': 'valgrind_parser'},
      package_data={'valgrind_parser': ['data/*.json']},
      include_package_data=True,
      install_requires=['json2table'],
      zip_safe=False
      )
