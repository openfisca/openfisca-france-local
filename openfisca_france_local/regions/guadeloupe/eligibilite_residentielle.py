from openfisca_france.model.base import Variable, Menage, MONTH

from openfisca_core.populations.population import Population
from openfisca_core.periods import Period

from numpy.core.defchararray import startswith

DEPARTEMENT_GUADELOUPE = [b'97']


class guadeloupe_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la région Guadeloupe."

    def formula(menage: Population, period: Period):
        depcom = menage('depcom', period)
        return sum([startswith(depcom, code) for code in DEPARTEMENT_GUADELOUPE]) > 0
