from __future__ import unicode_literals, print_function
from codecs import open
from os.path import dirname, join
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
import newrelic_marklogic_plugin


def read(fname):
    return open(join(dirname(__file__), fname)).read()

def main():
    setup(
        name='newrelic_marklogic_plugin',
        description='New Relic plugin for monitoring MarkLogic.',
        long_description=read('README.rst'),
        long_description_content_type='text/x-rst',
        version=newrelic_marklogic_plugin.__version__,
        packages=find_packages(),
        url='https://github.com/marklogic-community/newrelic-plugin',
        license='Apache License 2.0',
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
        scripts=[
            'scripts/newrelic_marklogic.py'
        ],
        platforms='any',
        install_requires=[
            'requests>=2.11.1'
        ]
    )


if __name__ == '__main__':
    main()
