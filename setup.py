from setuptools import setup
import sys


if sys.version_info < (2,5):
    raise NotImplementedError("Sorry, you need at least Python 2.5 \
        or Python 3.x to use cprofilev.")


setup(
    name='CProfileV',
    version='0.0.14',
    url='https://github.com/ymichael/cprofilev',
    author='Michael Yong',
    author_email='wrong92@gmail.com',
    py_modules=['cprofilev'],
    scripts = ['cprofilev.py'],
    install_requires=["bottle"],
    entry_points={
        'console_scripts': [
            'cprofilev = cprofilev.cprofilev:main',
        ]
    },
    license='MIT',
    description='Thin wrapper for viewing python cProfile output',
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
