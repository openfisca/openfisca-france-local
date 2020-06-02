 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore


class alfortville_noel_enfants_demo(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = u"Montant des ressources prises en compte pour le dispositif Noël des enfants"

    def formula(famille, period, parameters):
        period = period.last_month

        individual_resource_names = [
            'aah',
            'ass',
            'chomage_net',
            'retraite_nette',
            'salaire_net'
        ]
        individu_resources = sum([famille.members(resource, period) for resource in individual_resource_names])
 
        rsa = famille('rsa', period)
        return rsa + famille.sum(individu_resources)
