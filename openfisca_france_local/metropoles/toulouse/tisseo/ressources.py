 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, FoyerFiscal, YEAR, select

class tisseo_transport_reduction_ressources_fiscales(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR
    label = u"Base ressource fiscales pour les titres de transports Tisséo"

    def formula(foyer_fiscal, period):
        return foyer_fiscal('rfr', period) / foyer_fiscal('nbptr', period) / 12
