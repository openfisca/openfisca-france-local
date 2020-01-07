 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Menage, MONTH

from numpy.core.defchararray import startswith


class nouvelle_aquitaine_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = u"Éligibilité résidentielle d'un ménage aux dipositifs de la Nouvelle Aquitaine"

    def formula(menage, period):
        code_departements = [b'16',
          b'17',
          b'19',
          b'23',
          b'24',
          b'33',
          b'40',
          b'47',
          b'64',
          b'79',
          b'86',
          b'87'
          ]

        depcom = menage('depcom', period)
        return sum([startswith(depcom, code) for code in code_departements]) > 0
