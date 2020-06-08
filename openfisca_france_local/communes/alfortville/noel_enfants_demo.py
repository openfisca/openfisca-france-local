 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Menage, MONTH, Variable


class alfortville_noel_enfants_demo(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité au dispositif Noel des enfants d'Alfortville"

    def formula(menage, period, parameters):
        return menage('depcom', period) == b'94002'
