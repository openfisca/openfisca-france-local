# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH


class eure_et_loir_eligibilite_pretvehicule(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Prêt de véhicule"
    reference = "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/Reglement_pret_de_vehicules_juin_2019.pdf"

    def formula(individu, period):
        recoit_rsa = individu.famille('rsa', period) > 0
        reside_eure_et_loir = individu.menage('eure_loire_eligibilite_residence', period)

        return recoit_rsa * reside_eure_et_loir
