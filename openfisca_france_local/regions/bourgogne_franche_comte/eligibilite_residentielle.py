from openfisca_france.model.base import Variable, Menage, MONTH
from openfisca_core.populations.population import Population
from openfisca_core.periods import Period
from numpy.core.records import array as np_array
from numpy.core.defchararray import startswith

DEPARTEMENTS_BOURGOGNE_FRANCHE_COMTE = [
    b'21', b'25', b'39', b'58', b'70', b'71', b'89', b'90'
]


class bourgogne_franche_comte_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la région Bourgogne Franche-Comté"

    def formula(menage: Population, period: Period) -> np_array:
        depcom: np_array = menage('depcom', period)
        return sum([startswith(depcom, code_departement) for code_departement in DEPARTEMENTS_BOURGOGNE_FRANCHE_COMTE]) > 0
