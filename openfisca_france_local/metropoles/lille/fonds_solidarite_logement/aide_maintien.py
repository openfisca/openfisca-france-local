 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, FoyerFiscal, Menage, MONTH, YEAR

class metropole_lille_fonds_solidarite_logement_aide_maintien_eligibilite(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = u"Ménage éligible à l'aide au maintien du FSL de la Métropole de Lille"

    def formula(menage, period):
        return menage('metropole_lille_eligibilite_geographique', period)
