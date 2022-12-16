from openfisca_france.model.base import Variable, Menage, MONTH
from openfisca_core.populations.population import Population
from openfisca_core.periods import Period
from numpy.core.records import array as np_array
from numpy.core.defchararray import startswith


class nouvelle_aquitaine_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la Nouvelle Aquitaine"

    def formula(menage: Population, period: Period, parameters) -> np_array:
        depcom = menage('depcom', period)
        return sum([startswith(depcom, str.encode(code)) for code in parameters(period).regions.nouvelle_aquitaine.departements]) > 0
