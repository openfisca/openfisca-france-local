 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore


class garantie_jeune_neet(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = u"Variable de test pour l'extension"

    def formula(individu, period):
        not_in_employment = individu('salaire_net', period) == 0

        scolarite = individu('scolarite', period)
        activite = individu('activite', period)
        not_in_education = (scolarite == TypesScolarite.inconnue) * (activite != TypesActivite.etudiant)

        return not_in_employment * not_in_education
