from setuptools import setup, find_packages

import os
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
    long_description = f.read()

setup(name='valgrind_parser',
      version='1.1',
      description='The valgrind logs parser. Creates the html report from txt logs.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/siddheshsathe/Valgrind-Log-Parser',
      author='Siddhesh Sathe',
      author_email='siddheshsathe@rediffmail.com',
      licence='GNU General Public License v3.0',
      packages=find_packages('valgrind_parser'),
      package_dir={'':'valgrind_parser'},
      package_data={
            '': [''],
            'utils': ['*.json']
      },
      include_package_data=True,
      install_requires=['json2table'],
      zip_safe=False
)
