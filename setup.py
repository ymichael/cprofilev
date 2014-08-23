from setuptools import setup
import sys


if sys.version_info < (2,5):
    raise NotImplementedError("Sorry, you need at least Python 2.5 to use cprofilev.")

VERSION = '0.1.2'

__doc__ = """\
A thin wrapper for viewing python cProfile output.

It provides a simple html view of the pstats.Stats object that is generated
from when a python script is run with the -m cProfile flag.

"""


setup(
    name='CProfileV',
    version=VERSION,
    url='https://github.com/ymichael/cprofilev',
    author='Michael Yong',
    author_email='wrong92@gmail.com',
    py_modules=['cprofilev'],
    entry_points="""
    [console_scripts]
    cprofilev = cprofilev:main
    """,
    install_requires=["bottle"],
    license='MIT',
    description='Thin wrapper for viewing python cProfile output',
    long_description=__doc__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Framework :: Bottle',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ]
)
