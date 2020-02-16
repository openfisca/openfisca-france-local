 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, FoyerFiscal, Individu, MONTH, YEAR

class tisseo_transport_reduction(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Pourcentage de la réduction pour les abonnements sur le réseau Tisséo de la métropole de Toulouse"

    def formula(individu, period):
        return individu('tisseo_transport_jeune_reduction', period)
