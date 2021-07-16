# Extension OpenFisca pour nos partenariats avec les collectivités territoriales

[![Créer un environnement de travail dans Gitpod](https://camo.githubusercontent.com/1eb1ddfea6092593649f0117f7262ffa8fbd3017/68747470733a2f2f676974706f642e696f2f627574746f6e2f6f70656e2d696e2d676974706f642e737667)](https://gitpod-referer.now.sh/api/gitpod-referer-redirect)


## Introduction

[OpenFisca](https://www.openfisca.fr/) est un logiciel libre de micro-simulation. Ce dépôt contient la modélisation des aides locales françaises. Celles-ci enrichissent le modèle national de la France, [openfisca-france](https://github.com/openfisca/openfisca-france#openfisca-france).

Pour plus d'information sur les fonctionnalités et la manière d'utiliser OpenFisca, vous pouvez consulter la [documentation générale](https://openfisca.org/doc/).


## Installation

Ce paquet requiert [Python 3.7 ou supérieur](https://www.python.org/downloads/) et [pip](https://pip.pypa.io/en/stable/installing/).

Afin d'installer l'extension `openfisca-france-local`, lancez une fenêtre de terminal et suivez les instructions suivantes pour en récupérer le code source :

```shell
git clone git@github.com:betagouv/openfisca-france-local.git
```

Puis, pour aller dans `openfisca-france-local` et l'installer dans votre environnement :

```shell
cd openfisca-france-local
pip install --editable .
```

Une fois l'installation terminée, vous devriez pouvoir la tester avec les commandes suivantes :

```shell
openfisca test tests/test_dispositif.yml --country-package openfisca_france --extension openfisca_france_local
```

Ou plus simplement :

```shell
openfisca_local_test tests/test_dispositif.yml
```

Ceci exécute un test `test_dispositif.yml` faisant appel au module `openfisca_france_local`. Vous devriez obtenir un résultat se terminant par `1 passed in 0.0xs` tel que dans cet exemple :

```shell
libyaml is not installed in your environment. This can make OpenFisca slower to start. Once you have installed libyaml, run 'pip uninstall pyyaml && pip install pyyaml --no-cache-dir' so that it is used in your Python environment.

 libyaml is not installed in your environment, this can make your test suite slower to run. Once you have installed libyaml, run `pip uninstall pyyaml && pip install pyyaml --no-cache-dir` so that it is used in your Python environment.
=================== test session starts ===================
platform linux -- Python 3.7.4, pytest-5.1.2, py-1.8.0, pluggy-0.12.0
rootdir: /home/thomas/test/openfisca-france-local
collected 1 item                                          

tests/test_dispositif.yml .

==================== 1 passed in 0.01s ====================
```

:tada: openfisca-france-local est prêt à être utilisé !

### Rédaction des formules et tests

Vous trouverez un exemple d'aide dans le fichier [communes/alfortville/noel_enfants.py](https://github.com/betagouv/openfisca-france-local/blob/master/openfisca_france_local/communes/alfortville/noel_enfants.py#L57-L71), ainsi que le fichier de tests associé, [tests/communes/alfortville/noel_enfants.yml](https://github.com/betagouv/openfisca-france-local/blob/master/tests/communes/alfortville/noel_enfants.yml#L50-L56). Les paramètres nécessaires au calcul se trouvent quant à eux dans le fichier [openfisca_france_local/parameters/communes/alfortville.yml](https://github.com/betagouv/openfisca-france-local/blob/master/openfisca_france_local/parameters/communes/alfortville.yml).

Pour ajouter des formules et tests, créez simplement des fichiers .py et .yml à l'intérieur du répertoire.
