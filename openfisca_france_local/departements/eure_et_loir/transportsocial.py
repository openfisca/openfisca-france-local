# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH


class eure_et_loir_eligibilite_transportsocial(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Transport social"

    def formula(individu, period):
        reside_eure_et_loir = individu.menage('eure_et_loir_eligibilite_residence', period)
        recoit_rsa = individu.famille('rsa', period) > 0
        a_entre_18_28_ans = 18 <= individu.age <= 25
        revenue_inferieur_RSA = individu.revenus_nets_du_travail < rsa

        return reside_eure_et_loir * (recoit_rsa + reside_eure_et_loir * a_entre_18_28_ans * revenue_inferieur_RSA)
