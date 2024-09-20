from openfisca_france.model.base import Variable, Menage, MONTH
from numpy.core.defchararray import startswith


class meurthe_et_moselle_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de Meurthe-et-Moselle"

    def formula(menage, period):
        return startswith(menage('depcom', period), b'54')
