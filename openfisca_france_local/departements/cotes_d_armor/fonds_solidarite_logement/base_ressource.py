# -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore

def bareme_de_base(bareme, nb):
    return (nb > 0) * (select(
        [nb == 1, nb == 2, nb == 3, nb == 4, nb >= 5],
        [bareme.v1, bareme.v2, bareme.v3, bareme.v4, bareme.v5]
    ) + max_(0, nb - 5) * bareme.plus)

class cotes_d_armor_fonds_solidarite_logement_base_ressource_mensuelle(Variable):
    value_type = float
    entity = Menage
    definition_period = MONTH

    def formula(menage, period, parameters):
        individual_resource_names = [
            'aah',
            'ass',
            'chomage_net',
            'retraite_nette',
            'salaire_net'
        ]
        individu_resources = sum([menage.members(resource, period) for resource in individual_resource_names])

        family_resource_names = [
            'rsa',
            'ppa',
        ]
        famil_resources = sum([menage.members.famille(resource, period) for resource in family_resource_names])

        frs = menage.sum(famil_resources, role=Famille.DEMANDEUR)
        irs = menage.sum(individu_resources)
        return frs + irs

class cotes_d_armor_fonds_solidarite_logement_base_ressource_moyennee(Variable):
    value_type = float
    entity = Menage
    definition_period = MONTH

    def formula(menage, period, parameters):
        return menage('cotes_d_armor_fonds_solidarite_logement_base_ressource_mensuelle', period.last_3_months, options = [ADD]) / 3
