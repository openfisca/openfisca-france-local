from openfisca_france.model.base import Variable, MONTH, Individu
from numpy import select


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

        qf_max1 = benefit_parameters.tranche1.quotient_familial_maximum
        taux1 = benefit_parameters.tranche1.taux_de_reduction
        qf_max2 = benefit_parameters.tranche2.quotient_familial_maximum
        taux2 = benefit_parameters.tranche2.taux_de_reduction
        qf_max3 = benefit_parameters.tranche3.quotient_familial_maximum
        taux3 = benefit_parameters.tranche3.taux_de_reduction

        montant = select([qf <= qf_max1, qf <= qf_max2, qf <= qf_max3,
                         qf > qf_max2], [taux1, taux2, taux3, 0])
        return montant
