from openfisca_france.model.base import *


class bordeaux_aide_premiere_necessite_base_ressources(Variable):
    value_type = float
    entity = Menage
    definition_period = MONTH
    label = "Base ressources pour le calcul de l'aide de première nécessité de la ville de Bordeaux"

    def formula(menage, period):
        ressources = [
            # ressources d'activité
            'salaire_net',
            'indemnites_chomage_partiel',
            'remuneration_apprenti',
            'indemnites_volontariat',
            'revenus_stage_formation_pro',
            'bourse_recherche',
            'hsup',
            'etr',
            'rpns_auto_entrepreneur_benefice',
            'rsa_indemnites_journalieres_activite',
            # pensions
            'chomage_net',
            'retraite_nette',
        ]
        ressources_individu = menage.sum(sum([menage.members(r, period) for r in ressources]))

        return ressources_individu + menage.personne_de_reference.famille('rsa', period)


class bordeaux_aide_premiere_necessite_eligibilite(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité à l'aide de première nécessité de la ville de Bordeaux"

    def formula(menage, period, parameters):
        majeur = menage.personne_de_reference("majeur", period) + menage.conjoint("majeur", period)

        bordelais = menage('depcom', period) == b"33063"

        uc = menage('unites_consommation', period.this_year)
        ressources = menage('bordeaux_aide_premiere_necessite_base_ressources', period)
        seuil_de_pauvrete = parameters(period).communes.bordeaux.aide_premiere_necessite.seuil_de_pauvrete
        plafond = uc * seuil_de_pauvrete
        eligibilite_financiere = ressources <= plafond
        return bordelais * majeur * eligibilite_financiere
