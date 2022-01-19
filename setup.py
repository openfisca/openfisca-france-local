from setuptools import setup, find_packages


setup(
    name="OpenFisca-France-Local",
    version="2.1.0",
    author="OpenFisca Team",
    author_email="contact@openfisca.fr",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Information Analysis",
        ],
    description="Extension OpenFisca pour nos partenariats avec les collectivités territoriales",
    keywords="benefit france france-local microsimulation social tax",
    license="http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    url="https://github.com/openfisca/openfisca-france",

    packages=find_packages(),
    include_package_data=True,
    install_requires = [
        'OpenFisca-Core >= 35.2.0, < 36',
        'OpenFisca-France >= 102, < 104',
        'pandas == 1.0.3'
        ],
    extras_require = {
        'test': [
            'nose',
            ],
        'excel-reader': [
            'xlrd == 1.2.0'
            ]
        },
    scripts=['openfisca_france_local/scripts/openfisca_local_test']
)
