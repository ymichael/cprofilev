from setuptools import setup
import sys
import cprofilev


if sys.version_info < (2,5):
    raise NotImplementedError("Sorry, you need at least Python 2.5 \
        or Python 3.x to use cprofilev.")


setup(
    name='CProfileV',
    version=cprofilev.VERSION,
    url='https://github.com/ymichael/cprofilev',
    author='Michael Yong',
    author_email='wrong92@gmail.com',
    py_modules=['cprofilev'],
    entry_points="""
    [console_scripts]
    cprofilev = cprofilev.main
    """,
    install_requires=["bottle"],
    license='MIT',
    description='Thin wrapper for viewing python cProfile output',
    long_description=cprofilev.__doc__,
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
