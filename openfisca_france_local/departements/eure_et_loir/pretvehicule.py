# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH


class eure_et_loir_eligibilite_pretvehicule(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Pret de vehicule"

    def formula(individu, period):
        recoit_rsa = individu.famille('rsa', period) > 0
        reside_eure_et_loir = individu.menage('eure_et_loir_eligibilite_residence', period)

        return recoit_rsa * reside_eure_et_loir
