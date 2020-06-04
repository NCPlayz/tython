from setuptools import setup
import re

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('tython/__init__.py') as f:
    version = re.search("__version__ = '(.+)'", f.read()).group(1)

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='tython',
    author='NCPlayz',
    python_requires='>=3.6.0',
    url='https://github.com/FourStarBasement/tython',
    version=version,
    packages=['tython'],
    license='MIT',
    description='A simple TypeScript to Python transpiler.',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: JavaScript',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed'
    ]
)