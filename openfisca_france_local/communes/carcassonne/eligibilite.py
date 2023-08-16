from openfisca_france.model.base import Menage, MONTH, Variable


class carcassonne_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de Carcassonne"

    def formula(menage, period):
        return menage('depcom', period) == b'11069'
