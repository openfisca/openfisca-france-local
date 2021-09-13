# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH, not_, DIVIDE


class eure_et_loir_eligibilite_repas_foyer_personne_agee(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité à l'aide Repas Foyer pour les personnes âgées"
    reference = ["Titre 2 Chapitre 1-2 du règlement départementl d'Aide Sociale PA PH de l'Eure-et-Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RDAS_valide__decembre_2019.pdf"
                 ]
    documentation = """
                        Les personnes âgées peuvent bénéficier d’une prise en charge des frais de repas servis par des foyers restaurant créés par les communes, les CCAS ou les CIAS habilités à l’aide sociale. La participation financière du bénéficiaire est déterminée en fonction de ses ressources et du prix du repas.
                        Cette aide fait l’objet d’une récupération sur succession et n’est pas cumulable avec l’Allocation compensatrice pour tierce personne (ACTP), la Majoration Tierce Personne (MTP versée par la CPAM), l’Allocation personnalisée d’autonomie (APA), les prestations d’aide-ménagère servie par les caisses de retraite.
                    """

    def formula_2020_01(individu, period, parameters):
        age = individu('age', period)
        inapte_travail = individu('inapte_travail', period)
        ressortissant_eee = individu('ressortissant_eee', period)
        repas_foyer_parameters = parameters(
            period).departements.eure_et_loir.repas_foyer

        condition_residence = individu.menage('eure_et_loir_eligibilite_residence', period)
        condition_age = ((age >= repas_foyer_parameters.age_minimal_personne_agee_apte_travail) + (
            (age >= repas_foyer_parameters.age_minimal_personne_agee_inapte_travail) * inapte_travail))
        condition_nationalite = ressortissant_eee + individu('titre_sejour', period) + individu('refugie',period) + individu('apatride', period)
        condition_ressources = individu('asi_aspa_base_ressources_individu', period) <= individu.famille('aspa', period)

        condition_apa = individu('apa_domicile', period.last_month) <= 0
        condition_aides_actp = not_(individu('beneficiaire_actp', period))
        condition_aides_mtp = not_(individu('mtp', period))
        condition_aide_menagere_caisse_retraite = not_(individu('aide_menagere_fournie_caisse_retraite', period))
        conditions_non_cumul = condition_apa * condition_aide_menagere_caisse_retraite * condition_aides_actp * condition_aides_mtp

        return (
            condition_residence
            * condition_age
            * condition_nationalite
            * condition_ressources
            * conditions_non_cumul
            )


class eure_et_loir_eligibilite_repas_foyer_personne_handicapee(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité à l'aide Repas Foyer pour les personnes handicapées"
    reference = ["Titre 3 Chapitre 1-2 du règlement départementl d'Aide Sociale PA PH de l'Eure-et-Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RDAS_valide__decembre_2019.pdf"
                 ]
    documentation = """
                        Les personnes en situation de handicap peuvent bénéficier d’une prise en charge des frais de repas servis par des foyers restaurant créés par les communes, les CCAS ou les CIAS habilités à l’aide sociale. 
                        La participation financière du bénéficiaire est déterminée en fonction de ses ressources et du prix du repas.
                        Cette aide n’est pas cumulable avec l’Allocation compensatrice pour tierce personne (ACTP), la Majoration Tierce Personne (MTP versée par la CPAM) et les prestations d’aide-ménagère servies par les caisses de retraite.
                    """

    def formula_2020_01(individu, period, parameters):
        taux_incapacite = individu('taux_incapacite', period)
        restriction_substantielle_durable = individu('aah_restriction_substantielle_durable_acces_emploi', period)
        age = individu('age', period)
        ressortissant_eee = individu('ressortissant_eee', period)

        repas_foyer_parameters = parameters(
            period).departements.eure_et_loir.repas_foyer

        # Base de ressources identique à celle pour l'aide ménagère PH.
        individual_resource_names = {
            'aah',
            'salaire_imposable',
            'retraite_imposable',
            'pensions_invalidite',
            'revenus_stage_formation_pro'
        }
        ressources_famille = {'aspa'}
        ressources_annuelles = {'retraite_complementaire_artisan_commercant',
                                'retraite_complementaire_profession_liberale'
                                }
        individu_resources_month = sum(
            sum([individu(resource, period.last_month) for resource in individual_resource_names]),
            sum([individu.famille(resource, period.last_month) for resource in ressources_famille]))
        individu_resources = sum(individu_resources_month, sum(
            [individu(resource, period, options=[DIVIDE]) for resource in ressources_annuelles]))

        condition_residence = individu.menage('eure_et_loir_eligibilite_residence', period)
        condition_age = age < repas_foyer_parameters.age_minimal_personne_handicap
        condition_nationalite = ressortissant_eee + individu('titre_sejour', period) + individu('refugie',period) + individu('apatride', period)
        condition_taux_incapacite = ((taux_incapacite >= repas_foyer_parameters.taux_incapacite_superieur)
                                     + ((taux_incapacite <= repas_foyer_parameters.taux_incapacite_maximum_restriction_acces_emploi) * (
                                         (taux_incapacite >= repas_foyer_parameters.taux_incapacite_minimum_restriction_acces_emploi) * restriction_substantielle_durable)))
        condition_ressources = individu_resources <= individu.famille('aspa', period)

        condition_aides_actp = not_(individu('beneficiaire_actp', period))
        condition_aides_mtp = not_(individu('mtp', period))
        condition_aide_menagere_caisse_retraite = not_(individu('aide_menagere_fournie_caisse_retraite', period))
        conditions_non_cumul = condition_aide_menagere_caisse_retraite * condition_aides_actp * condition_aides_mtp

        return (
            condition_residence
            * condition_taux_incapacite
            * condition_nationalite
            * condition_age
            * conditions_non_cumul
            * condition_ressources
            )
