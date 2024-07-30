# Changelog

## [6.12.3] - 2024-07-30

_Pour les changements détaillés et les discussions associées, référencez la pull request [#212](https://github.com/openfisca/openfisca-france-local/pull/212)_

### Changed

- Met à jour la dépendance `OpenFisca-France` pour supporter les versions jusqu'à `< 169`.


## [6.12.2] - 2024-05-07

_Pour les changements détaillés et les discussions associées, référencez la pull request [#211](https://github.com/openfisca/openfisca-france-local/pull/211)_

### Changed

- Met à jour la dépendance `OpenFisca-France` pour supporter les versions jusqu'à `< 168`.

## [6.12.1] - 2024-04-18

_Pour les changements détaillés et les discussions associées, référencez la pull request [#210](https://github.com/openfisca/openfisca-france-local/pull/210)_

### Changed

- Met à jour la dépendance `OpenFisca-France` pour supporter les versions jusqu'à `< 165`.

## [6.12.0] - 2024-04-17

_Pour les changements détaillés et les discussions associées, référencez la pull request [#209](https://github.com/openfisca/openfisca-france-local/pull/209)_

### Added

- Ajoute la variable `ile_de_france_aide_achat_voiture_electrique`

## [6.11.9] - 2024-03-12

_Pour les changements détaillés et les discussions associées, référencez la pull request [#208](https://github.com/openfisca/openfisca-france-local/pull/208)_

## [6.11.8] - 2024-03-12

_Pour les changements détaillés et les discussions associées, référencez la pull request [#207](https://github.com/openfisca/openfisca-france-local/pull/207)_

### Changed

- Met à jour la dépendance `OpenFisca-France` pour supporter les versions jusqu'à `< 160`.

## [6.11.7] - 2024-02-22

_Pour les changements détaillés et les discussions associées, référencez la pull request [#206](https://github.com/openfisca/openfisca-france-local/pull/206)_

### Changed

- Met à jour la dépendance `OpenFisca-France` pour supporter les versions jusqu'à `< 159`.

## [6.11.6] - 2024-01-18

_Pour les changements détaillés et les discussions associées, référencez la pull request [#198](https://github.com/openfisca/openfisca-france-local/pull/198)_

### Added

- Ajoute un test qui assure que le fichier 'epcicom2020.xlsx' sera trouvé lors d'utilisation externe

## [6.11.5] - 2024-01-16

_Pour les changements détaillés et les discussions associées, référencez la pull request [#200](https://github.com/openfisca/openfisca-france-local/pull/200)_

### Fixed

- Corrige et affine les `type hints` de la `aides_jeunes_reform_dynamic`

## [6.11.4] - 2024-01-03

_Pour les changements détaillés et les discussions associées, référencez la pull request [#201](https://github.com/openfisca/openfisca-france-local/pull/201)_

### Added

- Ajoute un job dans la CI pour lancer les tests en `.py`

## [6.11.3] - 2023-12-12

_Pour les changements détaillés et les discussions associées, référencez la pull request [#197](https://github.com/openfisca/openfisca-france-local/pull/197)_

### Fixed

- Corrige des période de calculs de `RFR` et `RNI`

## [6.11.2] - 2023-12-06

_Pour les changements détaillés et les discussions associées, référencez la pull request [#194](https://github.com/openfisca/openfisca-france-local/pull/194)_

### Fixed

- Corrige le problème de la réforme dynamique qui ne crée qu'une condition lorsqu'un profil est présent plus d'une fois

## [6.11.1] - 2023-12-06

_Pour les changements détaillés et les discussions associées, référencez la pull request [#196](https://github.com/openfisca/openfisca-france-local/pull/196)_

### Fixed

- Corrige la periode dans la formule du dispositif `yvelines_aide_permis`

## [6.11.0] - 2023-12-03

_Pour les changements détaillés et les discussions associées, référencez la pull request [#193](https://github.com/openfisca/openfisca-france-local/pull/193)_

### Added

- Ajoute la variable `sous_contrat_engagement_jeune`

### Changed

- Modifie le calcul du dispositif Revenu Solidarite Jeune de la métropole de Lyon pour utiliser la nouvelle variable plutôt que le montant du CEJ

## [6.10.0] - 2023-11-28

_Pour les changements détaillés et les discussions associées, référencez la pull request [#186](https://github.com/openfisca/openfisca-france-local/pull/186)_

### Added

- Ajoute l'aide au permis du département des Yvelines

## [6.9.0] - 2023-11-27

_Pour les changements détaillés et les discussions associées, référencez la pull request [#189](https://github.com/openfisca/openfisca-france-local/pull/189)_

### Added

- Ajoute le dispositif Revenu Solidarite Jeune de la métropole de Lyon

## [6.8.0] - 2023-11-27

_Pour les changements détaillés et les discussions associées, référencez la pull request [#191](https://github.com/openfisca/openfisca-france-local/pull/191)_

### Added

- Ajoute la gestion de la condition attaches_to_institution dans la `aides_jeunes_reform_dynamic`

## [6.7.2] - 2023-11-27

_Pour les changements détaillés et les discussions associées, référencez la pull request [#192](https://github.com/openfisca/openfisca-france-local/pull/192)_

### Fixed

- Corrige le problème de chargement du fichier contenant les *epcis* de la réforme `epci_test_factory` introduit dans la release `6.7.1`

## [6.7.1] - 2023-11-21

_Pour les changements détaillés et les discussions associées, référencez la pull request [#190](https://github.com/openfisca/openfisca-france-local/pull/190)_

### Fixed

- Corrige le warning lié à l'utilisation de `ressource.path()` dans la réforme `epci_test_factory`

## [6.7.0] - 2023-11-15

_Pour les changements détaillés et les discussions associées, référencez la pull request [#188](https://github.com/openfisca/openfisca-france-local/pull/188)_

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
