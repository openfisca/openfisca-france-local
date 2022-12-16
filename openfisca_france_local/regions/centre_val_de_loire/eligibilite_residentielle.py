from openfisca_france.model.base import Variable, Menage, MONTH
from openfisca_core.populations.population import Population
from openfisca_core.periods import Period
from numpy.core.defchararray import startswith


class centre_val_de_loire_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la région centre val de loire"

    def formula(menage: Population, period: Period, parameters):
        depcom = menage('depcom', period)
        return sum([startswith(depcom, str.encode(code)) for code in parameters(period).regions.centre_val_de_loire.departements]) > 0
