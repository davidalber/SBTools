from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name="SBTools",
      version="0.5-r1",
      description="A manager for systems biology plug-ins.",
      long_description="""\
SBTools provides a convenient, unified interface for systems biology
tools written in Python.
""",
      author="David Alber",
      author_email="david_alber@nrel.gov",
      #url="",
      license="GPL",
      packages=find_packages(exclude=['tests']),
      install_requires=[],
      entry_points = {
        'console_scripts': ['sbtools = sbtools.sbtools:main'],
        'SBTools.plugins': ['About about = sbtools.builtins:About',
                            'File file = sbtools.builtins:File',
                            'Help help h ? = sbtools.builtins:Help'],
      },
      test_suite = "tests.tests.SBToolsTestSuite"
)

