
from openfisca_france.model.base import (
    Variable, Individu, MONTH)


class revenu_solidaire_jeune(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameter):
        age = individu('age', period)
        eligibilite_age = (age >= 18) * (age <= 24)
        return 420 * eligibilite_age
