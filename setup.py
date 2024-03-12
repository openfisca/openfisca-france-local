from setuptools import setup, find_namespace_packages


setup(
    name='OpenFisca-France-Local',
    version='6.11.7',
    author='OpenFisca Team',
    author_email='contact@openfisca.fr',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Information Analysis',
        ],
    description='Extension OpenFisca pour nos partenariats avec les collectivités territoriales',
    long_description_content_type='text/markdown',
    keywords='benefit france france-local microsimulation social tax',
    license='http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url='https://github.com/openfisca/openfisca-france-local',

    packages=find_namespace_packages(),
    include_package_data=True,
    install_requires=[
        'OpenFisca-Core >= 40.0.1, < 42',
        'OpenFisca-France >= 153.0.1, < 159',
        'pandas >= 1.5.3, <2.0'
        ],
    extras_require={
        'test': [
            'nose',
            ],
        'excel-reader': [
            'openpyxl == 3.1.2',
            ]
        },
    scripts=['openfisca_france_local/scripts/openfisca_local_test']
    )
