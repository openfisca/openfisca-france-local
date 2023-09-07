# Changelog

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
