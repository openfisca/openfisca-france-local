from openfisca_france.model.base import Variable, Menage, MONTH
from openfisca_core.populations.population import Population
from openfisca_core.periods import Period
from numpy.core.records import array as np_array
from numpy.core.defchararray import startswith

DEPARTEMENT_REUNION = [
    b'974',
]


class reunion_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la région Reunion"

    def formula(menage: Population, period: Period) -> np_array:
        depcom: np_array = menage('depcom', period)
        return sum([startswith(depcom, code_departement) for code_departement in DEPARTEMENT_REUNION]) > 0
