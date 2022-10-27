from openfisca_france.model.base import Individu, Variable, MONTH


class etat_eligibilite_bafa(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        contrainte_age = parameters(
            period).aides_jeunes.etat_eligibilite_bafa.age.min
        return individu('age', period) >= contrainte_age
