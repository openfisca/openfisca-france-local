 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, FoyerFiscal, Menage, MONTH, YEAR

class tisseo_ressort_territorial(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = u"Indicatrice du ressort territorial de Tisséo"

    def formula(menage, period):
        depcom = menage('depcom', period)
        return (depcom == b'31555')
