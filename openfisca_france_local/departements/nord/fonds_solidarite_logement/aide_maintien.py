 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, FoyerFiscal, Menage, MONTH, YEAR, not_


class nord_fonds_solidarite_logement_aide_maintien_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = u"Ménage situé sur le territoire éligible au FSL du département du Nord"

    def formula(menage, period):
        nord = menage('nord_eligibilite_residence', period)
        metropole = menage('metropole_lille_eligibilite_geographique', period)
        return nord * not_(metropole)


class nord_fonds_solidarite_logement_aide_maintien_eligibilite(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = u"Ménage éligible à l'aide au maintien du FSL du département du Nord"

    def formula(menage, period):
        return menage('nord_fonds_solidarite_logement_aide_maintien_eligibilite_residence', period)
