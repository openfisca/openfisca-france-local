from setuptools import setup, find_packages


setup(
    name="OpenFisca-France-Local",
    version="0.10.0",
    description="Extension OpenFisca pour nos partenariats avec les collectivités territoriales",
    license="http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    author="",
    packages=find_packages(),
    include_package_data=True,
    install_requires = [
        'OpenFisca-Core >= 25, < 35',
        'OpenFisca-France >= 47.1.0, < 53'
        ],
    extras_require = {
        'test': [
            'nose',
            ],
        'excel-reader': [
            'pandas == 1.0.3',
            'xlrd == 1.2.0'
            ]
        },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
    scripts=['openfisca_france_local/scripts/openfisca_local_test']
)
