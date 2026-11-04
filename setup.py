from setuptools import setup, find_namespace_packages


setup(
    name='OpenFisca-France-Local',
    version='6.18.0',
    author='OpenFisca Team',
    author_email='contact@openfisca.fr',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Scientific/Engineering :: Information Analysis',
        ],
    description='Extension OpenFisca pour nos partenariats avec les collectivités territoriales',
    long_description_content_type='text/markdown',
    keywords='benefit france france-local microsimulation social tax',
    license='http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url='https://github.com/openfisca/openfisca-france-local',

    python_requires='>= 3.11',
    packages=find_namespace_packages(),
    include_package_data=True,
    install_requires=[
        'OpenFisca-Core >= 43, < 47',
        'OpenFisca-France >= 169.0.0, < 177.0.0',
        'pandas >= 2.2.2, < 3.0'  # 2.2.2 : première version compatible numpy 2, https://pandas.pydata.org/docs/whatsnew/v2.2.2.html
        ],
    extras_require={
        'test': [
            'nose',
            ],
        'excel-reader': [
            'openpyxl == 3.1.5',
            ]
        },
    scripts=['openfisca_france_local/scripts/openfisca_local_test']
    )
