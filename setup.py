from setuptools import setup
setup(name='valgrind_parser',
      version='0.2.1',
      description='The valgrind logs parser. Creates the html report from txt logs.',
      url='https://github.com/siddheshsathe/Valgrind-Log-Parser',
      author='Siddhesh Sathe',
      author_email='siddheshsathe@rediffmail.com',
      licence='GNU General Public License v3.0',
      packages=['valgrind_parser'],
      install_requires=['json2table'],
      zip_safe=False
)
