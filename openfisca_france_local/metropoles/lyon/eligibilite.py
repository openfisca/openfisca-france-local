from openfisca_france.model.base import Variable, MONTH, Menage


class lyon_metropole_eligibilite_geographique(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité géographique de la métropole de Lyon"

    def formula(menage, period):
        return menage("menage_dans_epci_siren_200046977", period)
