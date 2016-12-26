#!/usr/bin/env python
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    README = readme_file.read()


install_requires = [
    'click',
    'PyYAML',
    'colorama',
    'termcolor',
    'jinja2',
    'inflector',
    'flywheel',
    'dynamo3'
]


setup(
    name='tight cli',
    version='0.1.0',
    description="Microframework",
    long_description=README,
    author="Michael McManus",
    author_email='michaeltightmcmanus@gmail.com',
    url='https://github.com/michaelorionmcmanus/tight-cli',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    license='MIT',
    include_package_data=True,
    package_dir={'tight_cli': 'tight_cli'},
    zip_safe=False,
    keywords='tight',
    entry_points={
        'console_scripts': [
            'tight = tight_cli.cli:main',
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
)
