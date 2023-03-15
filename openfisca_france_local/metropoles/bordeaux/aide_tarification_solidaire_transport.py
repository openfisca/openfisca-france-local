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

        qf_max = {
            i: benefit_parameters[f'tranche{i}'].quotient_familial_maximum
            for i in range(1, 4)}

        taux = {
            i: benefit_parameters[f'tranche{i}'].taux_de_reduction
            for i in range(1, 4)}

        montant = select([qf <= qf_max[1], qf <= qf_max[2], qf <= qf_max[3],
                         qf > qf_max[2]], [taux[1], taux[2], taux[3], 0])

        return montant
