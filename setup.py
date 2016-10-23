from __future__ import unicode_literals,print_function
from distutils.core import setup
from codecs import open
from os.path import dirname, join
from setuptools import setup, find_packages

def main():
    base_dir = dirname(__file__)
    setup(
        base_dir=dirname(__file__),
        name='newrelic_marklogic_plugin',
        description='NewRelic plugin for monitoring MarkLogic.',
        long_description=open(join(base_dir, 'README.rst'), encoding='utf-8').read(),
        version='0.2.6',
        packages=find_packages(),
        url='http://github.com/marklogic/newrelic_marklogic',
        license=open(join(base_dir, 'LICENSE'), encoding='utf-8').read(),
        author='James Fuller',
        author_email='jim.fuller@marklogic.com',
        classifiers=['Programming Language :: Python',
                     'Development Status :: 3 - Alpha',
                     'Natural Language :: English',
                     'Environment :: Console',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: Apache Software License',
                     'Operating System :: OS Independent',
                     'Topic :: Software Development :: Libraries :: Python Modules'
                     ],
        scripts = [
            'scripts/newrelic_marklogic.py'
        ],
        platforms='any',
        install_requires=[
            'requests>=2.11.1'
        ],
    )

if __name__ == '__main__':
    main()
