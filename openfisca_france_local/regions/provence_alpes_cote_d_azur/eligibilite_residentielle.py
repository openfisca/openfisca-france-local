from openfisca_france.model.base import Variable, Menage, MONTH
from openfisca_core.populations.population import Population
from openfisca_core.periods import Period
from numpy.core.records import array as np_array
from numpy.core.defchararray import startswith

DEPARTEMENTS_PROVENCE_ALPES_COTE_D_AZUR = [
    b'04',
    b'05',
    b'06',
    b'13',
    b'83',
    b'84',
]


class provence_alpes_cote_d_azur_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la région Provence Alpes Cote d'Azur"

    def formula(menage: Population, period: Period) -> np_array:
        depcom: np_array = menage('depcom', period)
        return sum([startswith(depcom, code_departement) for code_departement in DEPARTEMENTS_PROVENCE_ALPES_COTE_D_AZUR]) > 0