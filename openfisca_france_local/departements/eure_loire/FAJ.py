# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH


class eure_et_loir_eligibilite_FAJ(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité au Fond d'Aide aux Jeunes"

    def formula(individu, period, parameters):
        reside_eure_et_loir = individu.menage('eure_loire_eligibilite_residence', period)
        age = individu('age', period)
        a_entre_18_25_ans = (age >= 18) * (age <= 25)
        rsa = parameters(period).prestations.minima_sociaux.rsa
        revenue_inferieur_RSA = individu('eure_et_loir_revenus_nets_du_travail', period) < rsa.montant_de_base_du_rsa

        return reside_eure_et_loir * a_entre_18_25_ans * revenue_inferieur_RSA
