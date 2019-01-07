# -*- coding: utf-8 -*-

from openfisca_france.model.base import *
from openfisca_core import reforms


class simulation_reform(reforms.Reform):
    class date_simulation(Variable):
        value_type = date
        entity = Individu
        label = u"Date de la simulation"
        definition_period = MONTH

    def apply(self):
        self.add_variable(self.date_simulation)
