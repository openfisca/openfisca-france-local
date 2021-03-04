from openfisca_france.model.base import Variable, Individu, MONTH


class eure_et_loir_eligibilite_transportsocial(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Transport social"
    reference = "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/Procedure_transport_social_2019.pdf"

    def formula(individu, period, parameters):
        reside_eure_et_loir = individu.menage('eure_loire_eligibilite_residence', period)
        recoit_rsa = individu.famille('rsa', period) > 0
        a_entre_18_28_ans = 18 <= individu('age', period) <= 25
        rsa = parameters(period).prestations.minima_sociaux.rsa
        revenue_inferieur_RSA = individu('eure_et_loir_revenus_nets_du_travail', period) < rsa.montant_de_base_du_rsa

        return reside_eure_et_loir * (recoit_rsa + a_entre_18_25_ans * revenue_inferieur_RSA)