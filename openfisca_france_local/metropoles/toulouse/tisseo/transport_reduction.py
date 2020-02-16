 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, FoyerFiscal, Individu, MONTH, YEAR

class tisseo_transport_reduction(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Pourcentage de la réduction pour les abonnements sur le réseau Tisséo de la métropole de Toulouse"

    def formula(individu, period):
        ressort_territorial = individu.menage('tisseo_ressort_territorial', period)

        return ressort_territorial * individu('tisseo_transport_jeune_reduction', period)
