from setuptools import setup
import sys


if sys.version_info < (2,5):
    raise NotImplementedError(
        "Sorry, you need at least Python 2.5 to use cprofilev.")

VERSION = '1.0.5'

__doc__ = """\
An easier way to use cProfile.

Outputs a simpler html view of profiled stats.
Able to show stats while the code is still running!

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
    description='An easier way to use cProfile',
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
