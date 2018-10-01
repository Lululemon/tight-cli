#!/usr/bin/env python

# Copyright (c) 2017 lululemon athletica Canada inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    author="lululemon developers",
    url='https://github.com/lululemon/tight-cli',
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
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
    ],
)
