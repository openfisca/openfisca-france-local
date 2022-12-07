from openfisca_france.model.base import Variable, Menage, MONTH

from openfisca_core.populations.population import Population
from openfisca_core.periods import Period
from numpy.core.records import array as np_array

from numpy.core.defchararray import startswith

DEPARTEMENTS_HAUTS_DE_FRANCE = [b'02', b'59', b'60', b'62', b'80']


class hauts_de_france_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la région Hauts-de-France."

    def formula(menage: Population, period: Period) -> np_array:
        depcom: np_array = menage('depcom', period)
        return sum([startswith(depcom, code) for code in DEPARTEMENTS_HAUTS_DE_FRANCE]) > 0
