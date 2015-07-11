import os

from setuptools import setup

def read(filen):
    with open(filen, 'r') as fp:
        return fp.read()

# Using vbox, hard links do not work
if os.environ.get('USER','') == 'vagrant':
    del os.link

setup(
    name='podium',
    version='0.1',
    description='Generic application framework',
    long_description=read('README.md'),
    url='https://github.com/BasementCat/podium',
    author='Alec Elton',
    author_email='alec.elton@gmail.com',
    packages=['podium'],
    install_requires=[],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False
)