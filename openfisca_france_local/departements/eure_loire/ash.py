# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH, DIVIDE


class eure_et_loir_eligibilite_ash_personne_agee(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité d'une personne agée à l'aide sociale à l'hébergement en établisement"
    reference = ["Titre 2 Chapitre 2-1 du Règlement départemental d'Aide Sociale PA PH de l'Eure et Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RDAS_valide__decembre_2019.pdf"
                 ]
    documentation = """
                    L’aide sociale à l’hébergement en établissement s’adresse aux personnes résidant en EHPAD, en résidence autonomie ou en USLD et dont les ressources ne permettent pas de faire face aux frais d’hébergement. 
                    Les ressources de la personne (hors prestations familiales) sont récupérées dans la limite de 90% (AL et APL récupérées à 100%).
                    Cette aide fait l’objet d’une récupération sur succession.
                    """

    def formula_2020_01(individu, period, parameters):
        age = individu('age', period)
        inapte_travail = individu('inapte_travail', period)
        ressortissant_eee = individu('ressortissant_eee', period)
        individual_resource_names = {
            'retraite_brute',
            'pensions_alimentaires_percues',
            'revenus_locatifs'
        }
        individual_resource_names_annuelles = {
            'revenus_nets_du_capital'
        }

        ash_parameters = parameters(
            period).departements.eure_et_loir.ash

        individu_resources = sum([individu(resource, period.last_month) for resource in individual_resource_names])
        foyer_fiscal_resources = individu.foyer_fiscal('rente_viagere_titre_onereux_net', period, options=[DIVIDE])
        individu_resources_annuelles = sum([individu(resource, period, options=[DIVIDE]) for resource in individual_resource_names_annuelles])
        resources = sum(sum(individu_resources, foyer_fiscal_resources), individu_resources_annuelles)

        # les ressources des obligés alimentaires ne sont ici pas prises en compte
        condition_residence = individu.menage('eure_et_loir_eligibilite_residence', period)
        condition_age = ((age >= ash_parameters.age_minimal_personne_agee_apte_travail) + (
                (age >= ash_parameters.age_minimal_personne_agee_inapte_travail) * inapte_travail))
        condition_nationalite = ressortissant_eee + individu('titre_sejour', period) + individu('refugie', period) + individu('apatride', period)
        condition_ressources = resources <= individu.menage('loyer', period)

        # Attention le loyer ici est défini sur un mois alors que les tarifs des établissements sont journaliers
        # Auquel sera ajouté individu('dependance_tarif_etablissement_gir_5_6',period) * nb de jours * tarif_journalier

        return condition_residence * condition_age * condition_nationalite * condition_ressources


class eure_et_loir_eligibilite_ash_personne_handicap(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité d'une personne en sitaution de handicap à l'aide sociale à l'hébergement en établisement"
    reference = ["Titre 2 Chapitre 3-1 du Règlement départemental d'Aide Sociale PA PH de l'Eure et Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RDAS_valide__decembre_2019.pdf"
                 ]
    documentation = """
                    Toute personne âgée de 18 ans et plus, dont l’état de santé ou le handicap nécessite l’entrée en établissement social ou médico-social (hébergement permanent, hébergement temporaire, accueil de jour), peut bénéficier d’une prise en charge des frais de séjour en foyer d’hébergement, en foyer occupationnel, en foyer de vie, en foyer d’accueil médicalisé. Le bénéficiaire contribue aux frais de séjour dans des conditions définies dans le cadre du règlement départemental d’aide sociale. 
                    Cette aide doit faire l’objet d’une décision d’orientation de la Maison départementale de l’autonomie (MDA).
                    """

    def formula_2020_01(individu, period, parameters):
        age = individu('age', period)
        ressortissant_eee = individu('ressortissant_eee', period)
        situation_handicap = individu('handicap', period)
        ash_parameters = parameters(
            period).departements.eure_et_loir.ash

        condition_residence = individu.menage('eure_et_loir_eligibilite_residence', period)
        condition_age = (age >= ash_parameters.age_minimal_personne_handicapee)
        condition_nationalite = ressortissant_eee + individu('titre_sejour', period) + individu('refugie', period) + individu('apatride', period)
        condition_handicap = situation_handicap

        return condition_residence * condition_age * condition_nationalite * condition_handicap
