#!/usr/bin/env python

from distutils.core import setup

setup(name='rada',
      version='0.1',
      description='Ukrainian budget data parser and tagger',
      author='Ilya Petrov',
      author_email='ilya.muromec@gmail.com',
      url='https://github.com/muromec/budget2012',
      packages=['rada', ],
      license = "BSD",
      entry_points={
          'console_scripts': ['rada = rada:main'],
      },
      install_requires=[
        'consoleargs',
        'xlrd',
      ],
)
