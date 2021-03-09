from openfisca_france.model.base import Variable, FoyerFiscal, Menage, MONTH, YEAR, select


class nantes_metropole_tarification_solidaire_transport_eligibilite_geographique(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité géographique pour la tarification solidaire des transports de Nantes Métropole"

    def formula(menage, period):
        return menage('menage_dans_epci_siren_244400404', period)


class nantes_metropole_tarification_solidaire_transport_quotient_familial(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR
    label = "Quotient familial pour la tarification solidaire des transports de Nantes Métropole"

    def formula(foyer_fiscal, period):
        return foyer_fiscal('rfr', period) / 12 / foyer_fiscal('nbptr', period)


class nantes_metropole_tarification_solidaire_transport_montant(Variable):
    value_type = float
    entity = Menage
    definition_period = MONTH
    label = "Montant de la réduction pour la tarification solidaire des transports de Nantes Métropole"

    def formula(menage, period):
        aah = menage.sum(menage.members('aah', period))
        qf = menage.personne_de_reference.foyer_fiscal('nantes_metropole_tarification_solidaire_transport_quotient_familial', period.n_2)
        return select([(qf <= 350) + (aah > 0), qf <= 500, qf <= 600], [100, 90, 70], default=0)


class nantes_metropole_tarification_solidaire_transport(Variable):
    value_type = float
    entity = Menage
    definition_period = MONTH
    label = "La tarification solidaire des transports de Nantes Métropole"
    reference = [
        "https://data.nantesmetropole.fr/pages/algorithmes_nantes_metropole/"
        ]

    def formula(menage, period):
        metro = menage('nantes_metropole_tarification_solidaire_transport_eligibilite_geographique', period)
        montant = menage('nantes_metropole_tarification_solidaire_transport_montant', period)
        return montant * metro
