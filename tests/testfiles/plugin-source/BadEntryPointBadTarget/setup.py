from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name="BadEntryPointBadTarget",
      version="0.1",
      description="Plug-in to test that bad entry points are handled at plug-in load time. This plug-in has a bad entry-point target (the part on the right side of the equal sign of the entry point).",
      author="David Alber",
      author_email="david_alber@nrel.gov",
      license="GPL",
      packages=find_packages(exclude=['tests']),
      install_requires=['SBTools>=0.5a1.dev'],
      entry_points = {
        'SBTools.plugins': ['BadEntryPointBadTarget bad-entry = badentrypointbadtarget.badentrypointbadtarget:ABadEntryPointBadTarget'],
      },
)

