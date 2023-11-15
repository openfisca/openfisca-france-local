# Changelog
## [6.7.1] - 2023-11-15

_Pour les changements détaillés et les discussions associées, référencez la pull request [#190](https://github.com/openfisca/openfisca-france-local/pull/190)

### Fixed

- Corrige le warning lié à l'utilisation de `ressource.path()` dans la réforme `epci_test_factory`

## [6.7.0] - 2023-11-15

_Pour les changements détaillés et les discussions associées, référencez la pull request [#188](https://github.com/openfisca/openfisca-france-local/pull/188)

### Added

- Ajoute la compatibilité avec les versions 156 d'`OpenFisca-France`.

## [6.6.1] - 2023-11-13

_Pour les changements détaillés et les discussions associées, référencez la pull request [#187](https://github.com/openfisca/openfisca-france-local/pull/187)_

### Fixed

- Corrige le crash de la réforme dynamique lors des simulation en mode Tracing

## [6.6.0] - 2023-10-24

_Pour les changements détaillés et les discussions associées, référencez la pull request [#185](https://github.com/openfisca/openfisca-france-local/pull/185)_

### Changed

- Met à jour la dépendance `OpenFisca-France` pour supporter les versions jusqu'à `< 155`.

## [6.5.0] - 2023-09-22

_Pour les changements détaillés et les discussions associées, consultez la pull request [#184](https://github.com/openfisca/openfisca-france-local/pull/184)_

### Added

- Ajoute la variable `crous_aide_100_repas_gratuits`

## [6.4.1] - 2023-09-19

_Pour les changements détaillés et les discussions associées, consultez la pull request [#183](https://github.com/openfisca/openfisca-france-local/pull/183)_

### Fixed

- Corrige l'url du projet dans setup.py

## [6.4.0] - 2023-09-18

_Pour les changements détaillés et les discussions associées, consultez la pull request [#182](https://github.com/openfisca/openfisca-france-local/pull/182)_

### Added

- Ajoute le profil `beneficiaire_rsa`

### Fixed

- Corrige le crash dans le cas où le fichier d'aide ne contient pas la clé `profils`

## [6.3.0] - 2023-09-18

_Pour les changements détaillés et les discussions associées, consultez la pull request [#181](https://github.com/openfisca/openfisca-france-local/pull/181)_

### Added

- Ajoute la variable `nouvelle_aquitaine_aide_permis`

### Changed

- Créé un dossier pour les pour les paramètres de la `carte solidaire` de la région Nouvelle Aquitaine

### Removed

- Retire la compatibilité avec `openfisca-france` v153.0.1 et inférieur

## [6.2.0] - 2023-09-05

_Pour les changements détaillés et les discussions associées, consultez la pull request [#180](https://github.com/openfisca/openfisca-france-local/pull/180)_

### Added

- Ajoute la compatibilité avec `OpenFisca-France` v152.x et v153.x

## [6.1.0] - 2023-08-22

_Pour les changements détaillés et les discussions associées, consultez la pull request [#178](https://github.com/openfisca/openfisca-france-local/pull/178)_

### Added

- Ajoute la compatibilité avec `OpenFisca-France` v151.x

## [6.0.3] - 2023-08-17

_Pour les changements détaillés et les discussions associées, consultez la pull request [#177](https://github.com/openfisca/openfisca-france-local/pull/177)_

### Added

- Ajoute la possibilité de spécifier le chemin des aides à charger via la reform_dynamic par une variable d'environnement DYNAMIC_BENEFIT_FOLDER

## [6.0.2] - 2023-08-16

_Pour les changements détaillés et les discussions associées, consultez la pull request [#171](https://github.com/openfisca/openfisca-france-local/pull/171)_

### Fixed

- Corrige la formula de la variable `hauts_de_france_aide_garde_enfant` qui gérait mal un partie du calcul vectoriel et provoquait un crash dans certains cas.

## [6.0.1] - 2023-07-31

_Pour les changements détaillés et les discussions associées, consultez la pull request [#174](https://github.com/openfisca/openfisca-france-local/pull/174)_

### Changed

- Modifie l'implantation du paramètre taux_incapacité dans la réforme dynamique Aides-Jeunes, sans changement des résultats des calculs

## [6.0.0] - 2023-07-24

_Pour les changements détaillés et les discussions associées, consultez la pull request [#173](https://github.com/openfisca/openfisca-france-local/pull/173)_

### Added

- Ajoute la compatibilité avec `OpenFisca-Core` v41.x
- Ajoute la compatibilité avec `OpenFisca-France` v150.x

### Removed

- **Breaking:** retire la génération de documentation dans l'API Web à la suite de la mise à jour d'`openfisca-Core v41` ([OpenFisca-Core #1189](https://github.com/openfisca/openfisca-core/pull/1189))
