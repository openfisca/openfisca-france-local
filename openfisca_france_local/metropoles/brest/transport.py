from openfisca_france.model.base import *  # noqa analysis:ignore

from numpy import (logical_not as not_)

from openfisca_france_local.metropoles.brest.communes import communes


class residence_brest_metropole(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = u"Le lieu de résidence se situe dans une commune faisant partie de Brest métropole"

    def formula(individu, period):
        code_insee_commune = individu.menage('depcom', period)
        return sum([code_insee_commune == code_insee for code_insee in communes])


class brest_metropole_transport(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Tarification solidaire de Brest métropole"

    def formula(individu, period, parameters):
        pourcent = individu.famille('brest_metropole_transport_montant', period)

        return individu('residence_brest_metropole', period) * pourcent


class brest_metropole_transport_montant(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = u"Tarif mensuel solidaire de Brest métropole"

    def formula(famille, period, parameters):
        cmu_c = famille('cmu_c', period)
        quotient_familial_caf = famille('quotient_familial_caf', period)

        return (
             6.2 * (quotient_familial_caf <= 482) +
            15   * ((482 < quotient_familial_caf) * (quotient_familial_caf <= 573) + cmu_c * (573 < quotient_familial_caf)) +
            22.5 * (573 < quotient_familial_caf) * (quotient_familial_caf <= 728) * not_(cmu_c)
        )
