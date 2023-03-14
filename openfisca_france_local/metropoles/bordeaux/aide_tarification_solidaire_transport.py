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

        rfr = individu.foyer_fiscal('rfr', period.this_year)
        nbptr = individu.foyer_fiscal('nbptr', period.this_year)
        qf = rfr / 12 / nbptr

        montant = benefit_parameters.tranche3.taux_de_reduction
        max_eligible_qf = benefit_parameters.tranche3.quotient_familial_maximum
        return (qf <= max_eligible_qf) * montant
