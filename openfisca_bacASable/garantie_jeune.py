 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore


class garantie_jeune_neet(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = u"Variable NEET - Not in Employement, Education or Training"

    def formula(individu, period):
        not_in_employment = individu('salaire_net', period) == 0

        scolarite = individu('scolarite', period)
        activite = individu('activite', period)
        not_in_education = (scolarite == TypesScolarite.inconnue) * (activite != TypesActivite.etudiant)

        no_indemnites_stage = individu('indemnites_stage', period) == 0
        no_revenus_stage_formation_pro = individu('revenus_stage_formation_pro', period) == 0
        not_in_training = no_indemnites_stage * no_revenus_stage_formation_pro

        return not_in_employment * not_in_education * not_in_training
