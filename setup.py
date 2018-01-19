# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="OpenFisca-BrestMetropole",
    version="0.0.2",
    description="Extension OpenFisca pour Brest métropole",
    license="http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    author="",
    packages=find_packages(),
    include_package_data=True,
    install_requires = [
        'OpenFisca-Core >= 20, < 22',
        'OpenFisca-France >= 18.11, < 20.1'
        ],
    extras_require = {
        'test': [
            'nose',
            ]
        },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
