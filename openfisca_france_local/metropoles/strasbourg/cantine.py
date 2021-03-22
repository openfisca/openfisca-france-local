from openfisca_france.model.base import Variable, Menage, MONTH


class strasbourg_metropole_tarification_solidaire_cantine(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité géographique pour la tarification solidaire de la cantine de l'Eurométropole de Strasbourg"
    default_value = True 
    