 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, FoyerFiscal, Individu, MONTH, YEAR

class tisseo_transport_jeune_reduction(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Pourcentage de la réduction pour les jeunes"
