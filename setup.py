from setuptools import setup, find_packages
from src.version import VERSION

setup(
    name='CProfileV',
    version=VERSION,
    url='https://github.com/ymichael/cprofilev',
    author='Michael Yong',
    author_email='wrong92@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=["bottle"],
    entry_points="""
    [console_scripts]
    cprofilev = cprofilev:main
    """,
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
