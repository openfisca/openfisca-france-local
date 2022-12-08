from openfisca_france.model.base import Variable, Menage, MONTH
from openfisca_core.populations.population import Population
from openfisca_core.periods import Period
from numpy.core.records import array as np_array
from numpy.core.defchararray import startswith

DEPARTEMENTS_ILE_DE_FRANCE = [
    b'75',
    b'77',
    b'78',
    b'91',
    b'92',
    b'93',
    b'94',
    b'95',
]


class ile_de_france_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la région Ile de France"

    def formula(menage: Population, period: Period) -> np_array:
        depcom: np_array = menage('depcom', period)
        return sum([startswith(depcom, code_departement) for code_departement in DEPARTEMENTS_ILE_DE_FRANCE]) > 0
