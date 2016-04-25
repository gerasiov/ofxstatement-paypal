#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

version = '1.0.0'
with open('README.rst') as f:
    long_description = f.read()

setup(name='ofxstatement-paypal',
      version=version,
      author='Alexander Krasnukhin',
      author_email='the.malkolm@gmail.com',
      url='https://github.com/themalkolm/ofxstatement-paypal',
      description=('ofxstatement plugins for paypal'),
      long_description=long_description,
      license='Apache License 2.0',
      keywords=['ofx', 'ofxstatement', 'paypal'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'Natural Language :: English',
          'Topic :: Office/Business :: Financial :: Accounting',
          'Topic :: Utilities',
          'Environment :: Console',
          'Operating System :: OS Independent'
      ],
      packages=['ofxstatement', 'ofxstatement.plugins'],
      namespace_packages=['ofxstatement', 'ofxstatement.plugins'],
      entry_points={
          'ofxstatement': ['paypal = ofxstatement.plugins.paypal:PayPalPlugin']
      },
      install_requires=['ofxstatement'],
      test_suite='ofxstatement.plugins.tests',
      include_package_data=True,
      zip_safe=True
      )
