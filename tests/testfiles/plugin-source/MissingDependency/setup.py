from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name="MissingDependency",
      version="0.1",
      description="Plug-in to test that missing dependencies are handled at plug-in load time.",
      author="David Alber",
      author_email="david_alber@nrel.gov",
      license="GPL",
      packages=find_packages(exclude=['tests']),
      install_requires=['SBTools>=0.5a1.dev', 'blarg'],
      entry_points = {
        'SBTools.plugins': ['MissingDependency missing-dependency md = missingdependency.missingdependency:MissingDependency'],
      },
)

