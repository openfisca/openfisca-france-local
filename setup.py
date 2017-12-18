# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="Openfisca-RennesMetropole",
    version="1.0.5",
    description="Plugin OpenFisca pour les aides sociales de ma collectivité",
    license="http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    author="Rennes Métropole, Incubateur de Services Numériques (SGMAP)",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'OpenFisca-Core >= 20, < 21',
        'OpenFisca-France >= 18.11, < 20'
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
