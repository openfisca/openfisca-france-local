from openfisca_france.model.base import Variable, Menage, MONTH
from openfisca_core.populations.population import Population
from openfisca_core.periods import Period
from numpy.core.records import array as np_array
from numpy.core.defchararray import startswith

DEPARTEMENTS_CENTRE_VAL_DE_LOIRE = [b'18', b'28', b'36', b'37', b'41', b'45']


class centre_val_de_loire_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la région centre val de loire"

    def formula(menage: Population, period: Period) -> np_array:
        depcom: np_array = menage('depcom', period)
        return sum([startswith(depcom, code_departement) for code_departement in DEPARTEMENTS_CENTRE_VAL_DE_LOIRE]) > 0
