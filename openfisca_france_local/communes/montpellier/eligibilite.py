from openfisca_france.model.base import Menage, MONTH, Variable

class montpellier_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de Montpellier"

    def formula(menage, period):
        return menage('depcom', period) == b'34172'
