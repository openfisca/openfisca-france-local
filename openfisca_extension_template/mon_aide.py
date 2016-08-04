# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select, where)

from openfisca_france.model.base import *  # noqa analysis:ignore

class mon_aide(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Prestation locale qui consite à donner 100€ par mois et par enfants."

    def function(self, simulation, period):
        period = period.this_month
        nombre_enfants = simulation.calculate('af_nbenf', period)
        montant_par_enfant = simulation.legislation_at(period.start).ma_collectivite.mon_aide.montant

        return period, nombre_enfants * montant_par_enfant

