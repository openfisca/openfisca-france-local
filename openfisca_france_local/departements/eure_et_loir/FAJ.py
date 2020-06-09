# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH


class eure_et_loir_eligibilite_FAJ(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité au Fond d'Aide aux Jeunes"

    def formula(individu, period):
        reside_eure_et_loir = individu.menage('eure_et_loir_eligibilite_residence', period)
        a_entre_18_28_ans = 18 <= individu.age <= 25
        revenue_inferieur_RSA = individu.revenus_nets_du_travail < rsa

        return reside_eure_et_loir * a_entre_18_28_ans * revenue_inferieur_RSA
