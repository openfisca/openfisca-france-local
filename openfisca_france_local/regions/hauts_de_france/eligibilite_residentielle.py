from openfisca_france.model.base import Variable, Menage, MONTH

from openfisca_core.populations.population import Population
from openfisca_core.periods import Period

from numpy.core.defchararray import startswith


class hauts_de_france_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la région Hauts-de-France."

    def formula(menage: Population, period: Period, parameters):
        depcom = menage('depcom', period)
        return sum([startswith(depcom, str.encode(code)) for code in parameters(period).regions.hauts_de_france.departements]) > 0
