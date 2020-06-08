# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="OpenFisca-France-Local",
    version="0.0.3",
    description="Extension OpenFisca pour nos partenariats avec les collectivités territoriales",
    license="http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    author="",
    packages=find_packages(),
    include_package_data=True,
    install_requires = [
        'OpenFisca-Core >= 25, < 35',
        'OpenFisca-France >= 47.1.0, < 49',
        'pytest == 5.3.5'
        ],
    extras_require = {
        'test': [
            'nose',
            ]
        },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
    scripts=['openfisca_france_local/scripts/openfisca_local_test']
)
