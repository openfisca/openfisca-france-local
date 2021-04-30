from openfisca_france.model.base import *  # noqa analysis:ignore

from numpy import (logical_not as not_)

from openfisca_france_local.metropoles.brest.communes import communes


class quotient_familial_caf(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = u"Base ressources pour la tarification solidaire de Brest métropole"

    def formula(famille, period, parameters):

        base_ressources = famille('prestations_familiales_base_ressources', period)
        quotient_familial_caf_parts = famille('quotient_familial_caf_parts', period)

        return base_ressources / 12 / quotient_familial_caf_parts


class quotient_familial_caf_parts(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = u"Base ressources pour la tarification solidaire de Brest métropole"

    def formula(famille, period, parameters):
        en_couple = famille('en_couple', period)
        af_nbenf = famille('af_nbenf', period)
        nb_handicap = famille.sum(famille.members('handicap', period), role = Famille.ENFANT)

        return (
            not_(en_couple) * (
                1 + 
                1 * (af_nbenf >= 1)
            ) +
            en_couple * (
                2 + 
                0.5 * (af_nbenf >= 1)
            ) +
            (
                0.5 * (af_nbenf >= 2) +
                1   * (af_nbenf >= 3) +
                0.5 * (af_nbenf >= 4) * (af_nbenf - 3) +
                0.5 * nb_handicap
            )
        )
