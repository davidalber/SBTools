from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name="UnsatisfiedDependency",
      version="0.1",
      description="Plug-in to test that unsatisfied dependencies are handled at plug-in load time.",
      author="David Alber",
      author_email="david_alber@nrel.gov",
      license="GPL",
      packages=find_packages(exclude=['tests']),
      install_requires=['SBTools>=10.0'],
      entry_points = {
        'SBTools.plugins': ['UnsatisfiedDependency unsatisfied-dependency ud = unsatisfieddependency.unsatisfieddependency:UnsatisfiedDependency'],
      },
)

