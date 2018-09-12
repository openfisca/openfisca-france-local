 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore


class alfortville_cheque_noel(Variable):
    value_type = float
    entity = Famille
    definition_period = YEAR
    label = u"Montant"

    def formula(famille, period, parameters):
        cheque_noel = parameters(period).communes.alfortville.cheque_noel
        return cheque_noel.montant * (famille('af_nbenf', period.first_month) >= 0)
