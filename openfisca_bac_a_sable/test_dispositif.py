 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore


class test_dispositif(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = u"Variable de test pour l'extension"

    def formula(individu, period):
        return 1 * individu('age', period)
