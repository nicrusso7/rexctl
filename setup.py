import os
import platform
from distutils.core import setup

from pip._internal.req import parse_requirements
from setuptools import find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
os_name = platform.system()

with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_reqs = parse_requirements('requirements.txt', session='hack')
reqs = [str(ir.req) for ir in install_reqs]


def copy_assets(dir_path):
    base_dir = os.path.join('rexctl', dir_path)
    sep = '/'
    for (dirpath, dirnames, files) in os.walk(base_dir):
        for f in files:
            yield os.path.join(dirpath.split(sep, 1)[1], f)


setup(
    name='rexctl',
    version='0.0.1',
    license='Apache 2.0',
    packages=find_packages('rexctl'),
    package_dir={'': 'rexctl'},
    author='Nicola Russo',
    author_email='dott.nicolarusso@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nicrusso7/rexctl',
    download_url='https://github.com/nicrusso7/rexctl/archive/master.zip',
    install_requires=reqs,
    entry_points='''
        [console_scripts]
        rexctl=cli.entry_point:cli
    ''',
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
