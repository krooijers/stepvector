from setuptools import setup

setup(
    name='stepvector',

    version='0.4.0',

    description='python3 bottom-up implementation of stepvector',

    author='K. Rooijers',
    author_email='k.rooijers@hubrecht.eu',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='bioinformatics',

    py_modules=["stepvector"],

    install_requires=["sortedcontainers"],
)
