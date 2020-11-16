# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH
from openfisca_france.model.caracteristiques_socio_demographiques.demographie import ressortissant_eee
from openfisca_france.model.prestations.autonomie import TypesGir


class eure_et_loir_aide_menagere_personne_agee(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité d'une personne agée à l'aide sociale à domicile pour l'aide ménagère"
    reference = """ Titre 2 Chapitre 1-1 du Règlement départemental d'Aide Sociale PA PH de l'Eure et Loir
                    L’aide-ménagère est une aide en nature accordée aux personnes âgées qui, du fait de leur état de santé ou de leur âge, ont besoin de recourir à un personnel pour effectuer les actes de la vie courante. La participation financière du bénéficiaire est définie par le Conseil départemental.
                    L’éligibilité de l’aide dépend niveau de GIR (5 ou 6).
                    Cette aide fait l’objet d’une récupération sur succession et n’est pas cumulable avec l’Allocation compensatrice pour tierce personne (ACTP), la Majoration Tierce Personne (MTP versée par la CPAM), l’Allocation personnalisée d’autonomie (APA), les prestations d’aide-ménagère servie par les caisses de retraite.
                """

    def formula_2020_01(individu, period,parameters):
        age = individu('age', period)
        inapte_travail = individu('inapte_travail', period)
        ressortissant_eee =  individu('ressortissant_eee', period)
        gir = individu('gir', period)
        individual_resource_names = {
            'ass',
            'chomage_net',
            'retraite_nette',
            'salaire_net',
            'allocation_securisation_professionnelle',
            'dedommagement_victime_amiante',
            'gains_exceptionnels',
            'indemnites_chomage_partiel',
            'indemnites_journalieres',
            'indemnites_volontariat',
            'pensions_invalidite',
            'prestation_compensatoire',
            'prime_forfaitaire_mensuelle_reprise_activite',
            'retraite_brute',
            'revenus_stage_formation_pro',
            'rsa_base_ressources_patrimoine_individu'
        }

        individu_resources = sum([individu(resource, period.last_month) for resource in individual_resource_names])
        condition_age = ((age > parameters(period).departements.eure_et_loir.aide_menagere.age_minimal_personne_agee_apte_travail) or (age > parameters(period).departements.eure_et_loir.aide_menagere.age_minimal_personne_agee_inapte_travail and inapte_travail))
        condition_nationalite = ressortissant_eee
        condition_gir = ((gir == TypesGir.gir_5) or (gir == TypesGir.gir_6))
        condition_ressources = individu_resources < individu('asi_aspa_base_ressources_individu', period)
        conditions_aides = not individu('apa_eligibilite', period.last_month)
        return condition_age * condition_nationalite * condition_gir * condition_ressources * conditions_aides

class eure_et_loir_aide_menagere_personne_handicap(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité d'une personne en situation de handicap à l'aide ménagère à domicile"
    reference = """ Titre 3 Chapitre 1-1 du Règlement départemental d'Aide Sociale PA PH de l'Eure et Loir
                    L’aide-ménagère est accordée aux personnes en situation de handicap ayant besoin, pour demeurer à leur domicile, d’une aide matérielle pour effectuer les actes de la vie courante. 
                    La participation financière du bénéficiaire est définie par le Conseil départemental.
                    Cette aide n’est pas cumulable avec l’Allocation compensatrice pour tierce personne (ACTP), la Majoration Tierce Personne (MTP versée par la CPAM) et les prestations d’aide-ménagère servies par les caisses de retraite
                """

    def formula_2020_01(individu, period,parameters):
        taux_incapacite = individu('taux_incapacite', period)
        restriction_substantielle_durable = individu('aah_restriction_substantielle_durable_acces_emploi',period)
        age = individu('age', period)
        ressortissant_eee = individu('ressortissant_eee', period)
        individual_resource_names = {
            'ass',
            'chomage_net',
            'retraite_nette',
            'salaire_net',
            'allocation_securisation_professionnelle',
            'dedommagement_victime_amiante',
            'gains_exceptionnels',
            'indemnites_chomage_partiel',
            'indemnites_journalieres',
            'indemnites_volontariat',
            'pensions_invalidite',
            'prestation_compensatoire',
            'prime_forfaitaire_mensuelle_reprise_activite',
            'retraite_brute',
            'revenus_stage_formation_pro',
            'rsa_base_ressources_patrimoine_individu'
        }

        individu_resources = sum([individu(resource, period.last_month) for resource in individual_resource_names])
        condition_taux_incapacite = ((taux_incapacite >= parameters(period).departements.eure_et_loir.aide_menagere.taux_incapacite_superieur)
                                     or (taux_incapacite< parameters(period).departements.eure_et_loir.aide_menagere.taux_incapacite_maximum_avec_restriction_acces_emploi and taux_incapacite>parameters(period).departements.eure_et_loir.aide_menagere.taux_incapacite_minimum_avec_restriction_acces_emploi and restriction_substantielle_durable))
        condition_age = (age < parameters(period).departements.eure_et_loir.aide_menagere.age_minimal_personne_handicap)
        condition_nationalite = ressortissant_eee
        condition_ressources = individu_resources < individu('asi_aspa_base_ressources_individu', period)

        return condition_taux_incapacite * condition_age * condition_nationalite * condition_ressources