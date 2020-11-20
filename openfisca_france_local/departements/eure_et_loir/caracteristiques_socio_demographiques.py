from openfisca_france.model.base import Variable, Individu, MONTH

class titre_sejour(Variable):
    value_type = bool
    label ="Bénéficiaire d'un titre de séjour"
    entity = Individu
    definition_period = MONTH
    default_value = False
