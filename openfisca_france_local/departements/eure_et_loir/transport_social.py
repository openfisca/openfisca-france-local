from openfisca_france.model.base import Variable, Individu, MONTH


class eure_et_loir_eligibilite_transport_social(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité à l'aide de transport social"
    reference = "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/Procedure_transport_social_2019.pdf"

    def formula(individu, period, parameters):
        reside_eure_et_loir = individu.menage('eure_et_loir_eligibilite_residence', period)
        recoit_rsa = individu.famille('rsa', period) > 0
        age = individu('age', period)
        a_entre_18_25_ans = (18 <= age) * (age <= 25)
        rsa = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.rsa.rsa_m
        revenus_inferieurs_rsa = individu('eure_et_loir_revenus_nets_du_travail', period) < rsa.montant_de_base_du_rsa

        return reside_eure_et_loir * (recoit_rsa + a_entre_18_25_ans * revenus_inferieurs_rsa)
