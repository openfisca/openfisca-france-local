 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Famille, Individu, Menage, MONTH, Variable


class alfortville_noel_enfants_base_ressources(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Montant des ressources prises en compte pour le dispositif Noël des enfants"

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


class alfortville_noel_enfants_eligibilite_financiere(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Montant maximum des ressources pour bénéficier du chèque Noël des enfants"

    def formula(famille, period, parameters):
        smic = parameters(period).marche_travail.salaire_minimum.smic
        smic_brut_mensuel = smic.smic_b_horaire * smic.nb_heures_travail_mensuel
        # Utilisation des valeurs indicatives de service-public.fr pour passer du SMIC brut au SMIC net
        # https://www.service-public.fr/particuliers/vosdroits/F2300
        # Dans l'attente de la formule effectivement utilisée par la ville d'Alfortville
        smic_net_mensuel = 7.82 / 9.88 * smic_brut_mensuel

        base_ressources = famille('alfortville_noel_enfants_base_ressources', period)
        return base_ressources <= smic_net_mensuel


class alfortville_noel_enfants_eligibilite_jeune(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibité d'un enfant au dispositif Noël des enfants"

    def formula(individu, period, parameters):
        cheque_noel = parameters(period).communes.alfortville.cheque_noel
        age = individu('age', period)
        return age <= cheque_noel.age_maximum


class alfortville_noel_enfants(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Montant total des bons d'achats du disposition Noël des enfants pour une famille"

    def formula(famille, period, parameters):
        cheque_noel = parameters(period).communes.alfortville.cheque_noel

        residence_alfortville = famille.demandeur.menage('alfortville_eligibilite_residence', period)
        eligibilite_financiere = famille('alfortville_noel_enfants_eligibilite_financiere', period)

        enfants_eligibles = famille.members('alfortville_noel_enfants_eligibilite_jeune', period)
        nb_enfants_eligibles = famille.sum(enfants_eligibles)
        return residence_alfortville * eligibilite_financiere * cheque_noel.montant * nb_enfants_eligibles
