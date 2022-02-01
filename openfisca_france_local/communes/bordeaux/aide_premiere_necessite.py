from openfisca_france.model.base import Variable, Individu, MONTH


class bordeaux_aide_premiere_necessite_base_ressources(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Base ressources pour le calcul de l'aide de première nécessité de la ville de Bordeaux"


class bordeaux_aide_premiere_necessite_eligibilite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité à l'aide de première nécessité de la ville de Bordeaux"

    def formula(individu, period):
        return individu.menage('depcom', period) == b"33063"
