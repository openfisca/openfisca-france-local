# Contribuer à OpenFisca-France-Local

Avant tout, merci de votre volonté de contribuer au bien commun qu'est OpenFisca !

Afin de faciliter la réutilisation d'OpenFisca et d'améliorer la qualité du code, les contributions à OpenFisca suivent certaines règles.

Certaines règles sont communes à tous les dépôts OpenFisca et sont détaillées dans [la documentation générale](https://openfisca.org/doc/contribute/guidelines.html).

## Gestion sémantique de version

Le niveau des évolutions d'OpenFisca-France-Local doivent pouvoir être comprises par des réutilisateurs qui n'interviennent pas nécessairement sur le code.

Un numéro de version doit donc être attribué à toute évolution intégrée sur la branche principale `master` (par la mise à jour du fichier `setup.py`). Ses règles d'incrémentation suivent les principes du versionnement sémantique détaillés dans [la documentation générale](https://openfisca.org/doc/contribute/semver.html).

## Formalisation du CHANGELOG

Chaque version donne lieu à une description des changements qu'elle apporte dans le fichier `CHANGELOG.md`, fichier qui respecte le standard [Common Changelog](https://common-changelog.org).

La syntaxe à utiliser pour une entrée valide est détaillée dans [le wiki](https://github.com/openfisca/openfisca-france-local/wiki/Ajouter-une-entr%C3%A9e-dans-le-CHANGELOG).

Chaque Pull Request acceptée sur la branche principale déclenche le déploiement d'une nouvelle version.
