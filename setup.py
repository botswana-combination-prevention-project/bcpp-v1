# -*- coding: utf-8 -*-
import os
from setuptools import setup
from setuptools import find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
<<<<<<< HEAD
    name='bhp066',
=======
    name='bcpp',
>>>>>>> 73c7e0a48cefa68dad84c04c386126c2a55b89f3
    version='1.11.68',
    author=u'Botswana-Harvard AIDS Institute',
    author_email='ew2789@gmail.com',
    packages=find_packages(),
    include_package_data=True,
<<<<<<< HEAD
    url='http://github/botswana-harvard/edc',
    license='GPL license, see LICENSE',
    description='bhp066 bcpp edc',
=======
    url='http://github/botswana-harvard/bcpp',
    license='GPL license, see LICENSE',
    description='Botswana Combination Prevention Project (BHP066)',
>>>>>>> 73c7e0a48cefa68dad84c04c386126c2a55b89f3
    long_description=README,
    zip_safe=False,
    keywords='django EDC Botswana Combination Prevention Project BCPP BHP066',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
