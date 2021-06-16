#!/usr/bin/env python3
import typing
import setuptools
import os


BASE_DIR = os.path.dirname(__file__)


def read_all(name: str) -> str:
    with open(os.path.join(BASE_DIR, name)) as f:
        return f.read()


def read_requirements(path: str) -> typing.List[str]:
    return [
        line.strip()
        for line in read_all('requirements.txt').split('\n')
        if not line.startswith('#') and line.strip()
    ]


def main():
    setuptools.setup(
        name='python-yah',
        version='1.0.2',
        description='Yandex smart home apis',
        long_description=read_all('README.md'),
        long_description_content_type='text/markdown',
        url='https://github.com/sunsx0/yah',
        packages=setuptools.find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3',
        ],
        install_requires=read_requirements('requirements.txt'),
    )


if __name__ == '__main__':
    main()
