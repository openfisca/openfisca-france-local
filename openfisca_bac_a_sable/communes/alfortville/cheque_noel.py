 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore


class alfortville_cheque_noel_base_ressources(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = u"Montant des ressources prises en compte pour le dispositif Noël des enfants"


class alfortville_cheque_noel_eligibilite_financiere(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = u"Montant maximum des ressources pour bénéficier du chèque Noël des enfants"

    def formula(famille, period, parameters):
        smic = parameters(period).cotsoc.gen
        smic_brut_mensuel = smic.smic_h_b * smic.nb_heure_travail_mensuel
        smic_net_mensuel = 0.7 * smic_brut_mensuel

        base_ressources = famille('alfortville_cheque_noel_base_ressources', period)
        return base_ressources <= smic_net_mensuel


class alfortville_cheque_noel_eligibilite_jeune(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = u"Éligibité d'un enfant au dispositif Noël des enfants"

    def formula(individu, period, parameters):
        cheque_noel = parameters(period).communes.alfortville.cheque_noel
        age = individu('age', period)
        return age <= cheque_noel.age_maximum


class alfortville_cheque_noel(Variable):
    value_type = float
    entity = Famille
    definition_period = YEAR
    label = u"Montant"

    def formula(famille, period, parameters):
        cheque_noel = parameters(period).communes.alfortville.cheque_noel
        return cheque_noel.montant * (famille('af_nbenf', period.first_month) >= 0)
