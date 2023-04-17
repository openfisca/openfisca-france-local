from openfisca_france.model.base import Variable, MONTH, Individu


class bordeaux_metropole_aide_tarification_solidaire_transport(Variable):
    entity = Individu
    definition_period = MONTH
    value_type = float
    label = "Éligibilité à l'aide tarification solidaire le la métropole de Bordeaux"
    reference = [
        'https://tarificationsolidaire.bordeaux-metropole.fr/Accueil.aspx']

    def formula(individu, period, parameters):
        benefit_parameters = parameters(
            period).metropoles.bordeaux.aide_tarification_solidaire_transport

        rfr = individu.foyer_fiscal('rfr', period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period.n_2)
        quotient_familial = rfr / 12 / nbptr

        return benefit_parameters['tranches_taux_de_reduction_par_quotient_familial'].calc(quotient_familial)
