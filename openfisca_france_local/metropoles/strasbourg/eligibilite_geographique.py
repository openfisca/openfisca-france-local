from openfisca_france.model.base import Variable, Menage, MONTH


class strasbourg_metropole_eligibilite_geographique(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité géographique pour la tarification solidaire de la cantine de l'Eurométropole de Strasbourg"
    
    def formula(menage, period):
        return menage('menage_dans_epci_siren_246700488', period)
