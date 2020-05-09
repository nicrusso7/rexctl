import os
from distutils.core import setup

from setuptools import find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read()


setup(
    name='core',
    version='0.0.1',
    license='Apache 2.0',
    packages=find_packages('core'),
    package_dir={'': 'core'},
    author='Nicola Russo',
    author_email='dott.nicolarusso@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nicrusso7/rexctl',
    download_url='https://github.com/nicrusso7/rexctl/archive/master.zip',
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        rexctl=cli.entry_point:cli
    ''',
    package_data={
        'webserver': ['scripts/*'],
        'util': ['sim/*', 'templates/*']
    },
    keywords=['robot', 'quadruped', 'ai', 'reinforcement learning', 'machine learning', 'RL',
              'ML', 'tensorflow', 'spotmicro', 'rex'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Framework :: Robot Framework :: Library',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7']
)
