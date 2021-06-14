 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, FoyerFiscal, Individu, MONTH, YEAR, max_
from openfisca_france.model.prestations.education import TypesScolarite

class tisseo_transport_jeune_reduction(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Pourcentage de la réduction pour les jeunes"

    def formula(individu, period):
        age = individu('age', period)

        return (
          (4 < age) * ( age < 20) * 80 +
          (20 <= age) * ( age < 26) * 70
          )

class tisseo_transport_etudiant_reduction(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Pourcentage de la réduction pour les jeunes"

    def formula(individu, period):
        age = individu('age', period)

        scolarite = individu('scolarite', period)
        scolaire = (scolarite == TypesScolarite.lycee) + (scolarite == TypesScolarite.college)

        etudiant = individu('etudiant', period)
        eligible = scolaire + etudiant
        aide_non_boursier = (20 <= age) * ( age < 26) * eligible * 80

        boursier = individu('boursier', period)
        bourse_criteres_sociaux_echelon = individu('bourse_criteres_sociaux_echelon', period)
        aide_boursier = etudiant * boursier * (bourse_criteres_sociaux_echelon == 7) * (age < 35) * 100

        return max_(
          aide_boursier,
          aide_non_boursier
        )