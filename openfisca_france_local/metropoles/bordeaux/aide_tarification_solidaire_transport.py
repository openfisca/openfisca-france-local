from openfisca_france.model.base import Variable, MONTH, Individu, Menage


class bordeaux_metropole_aide_tarification_solidaire_transport_eligibilite_geographique(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité géographique à l'aide tarification solidaire de la métropole de Bordeaux"

    def formula(menage, period):
        return menage("menage_dans_epci_siren_243300316", period)


class bordeaux_metropole_aide_tarification_solidaire_transport(Variable):
    entity = Individu
    definition_period = MONTH
    value_type = float
    label = "Éligibilité à l'aide tarification solidaire de la métropole de Bordeaux"
    reference = [
        'https://tarificationsolidaire.bordeaux-metropole.fr/Accueil.aspx']

    def formula(individu, period, parameters):
        benefit_parameters = parameters(
            period).metropoles.bordeaux.aide_tarification_solidaire_transport

        rfr = individu.foyer_fiscal('rfr', period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period.n_2)
        quotient_familial = rfr / 12 / nbptr
        eligibilite_geographique = individu.menage('bordeaux_metropole_aide_tarification_solidaire_transport_eligibilite_geographique', period)

        return eligibilite_geographique * benefit_parameters['tranches_taux_de_reduction_par_quotient_familial'].calc(quotient_familial)
