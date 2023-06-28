from openfisca_france.model.base import Variable, Menage, MONTH

from numpy.core.defchararray import startswith


class haute_saone_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la Haute-Saone"

    def formula(menage, period):
        return startswith(menage('depcom', period), str.encode('70'))
