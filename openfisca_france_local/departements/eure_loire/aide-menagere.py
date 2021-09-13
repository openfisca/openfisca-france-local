# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH, not_, DIVIDE
from openfisca_france.model.prestations.autonomie import TypesGir


class aide_menagere_fournie_caisse_retraite(Variable):
    value_type = bool
    label = "Bénéficiaire de prestations d’aide-ménagère servie par les caisses de retraite"
    entity = Individu
    definition_period = MONTH
    default_value = False


class eure_et_loir_eligibilite_aide_menagere_personne_agee(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité d'une personne âgée à l'aide sociale à domicile pour l'aide ménagère"
    reference = [
        "Titre 2 Chapitre 1-1 du Règlement départemental d'Aide Sociale PA/PH de l'Eure-et-Loir",
        "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RDAS_valide__decembre_2019.pdf"
    ]
    documentation = """
                    L’aide-ménagère est une aide en nature accordée aux personnes âgées qui, du fait de leur état de santé ou de leur âge, ont besoin de recourir à un personnel pour effectuer les actes de la vie courante. La participation financière du bénéficiaire est définie par le Conseil départemental.
                    L’éligibilité de l’aide dépend niveau de GIR (5 ou 6).
                    Cette aide fait l’objet d’une récupération sur succession et n’est pas cumulable avec l’Allocation compensatrice pour tierce personne (ACTP), la Majoration Tierce Personne (MTP versée par la CPAM), l’Allocation personnalisée d’autonomie (APA), les prestations d’aide-ménagère servie par les caisses de retraite.
                    """

    def formula_2020_01(individu, period, parameters):
        age = individu('age', period)
        inapte_travail = individu('inapte_travail', period)
        ressortissant_eee = individu('ressortissant_eee', period)
        gir = individu('gir', period)
        possede_actp = individu('beneficiaire_actp', period)
        possede_mtp = individu('mtp', period)

        parameters_chemin = parameters(
            period).departements.eure_et_loir.aide_menagere

        condition_residence = individu.menage('eure_et_loir_eligibilite_residence', period)
        condition_age = ((age >= parameters_chemin.age_minimal_personne_agee_apte_travail) + (
                (age >= parameters_chemin.age_minimal_personne_agee_inapte_travail) * inapte_travail))
        condition_nationalite = ressortissant_eee + individu('refugie', period) + individu('apatride', period)

        # condition non intégrée : Les personnes de nationalité étrangère doivent justifier d'une résidence
        # en France métropolitaine ininterrompue depuis au moins 15 ans, et ce avant l'âge de 70 ans.
        condition_gir = ((gir == TypesGir.gir_5) + (gir == TypesGir.gir_6))
        condition_ressources = individu('asi_aspa_base_ressources_individu', period) <= individu.famille('aspa', period)

        condition_apa = individu('apa_domicile', period.last_month) <= 0
        condition_aides_actp = not_(possede_actp)
        condition_aides_mtp = not_(possede_mtp)
        condition_aide_menagere_caisse_retraite = not_(individu('aide_menagere_fournie_caisse_retraite', period))
        conditions_aides = condition_apa * condition_aide_menagere_caisse_retraite * condition_aides_actp * condition_aides_mtp

        return condition_residence * condition_age * condition_nationalite * condition_gir * condition_ressources * conditions_aides


class eure_et_loir_eligibilite_aide_menagere_personne_handicap(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité d'une personne en situation de handicap à l'aide ménagère à domicile"
    reference = [
        "Titre 3 Chapitre 1-1 du Règlement départemental d'Aide Sociale PA/PH de l'Eure-et-Loir",
        "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RDAS_valide__decembre_2019.pdf"
    ]
    documentation = """L’aide-ménagère est accordée aux personnes en situation de handicap ayant besoin, pour demeurer à leur domicile, d’une aide matérielle pour effectuer les actes de la vie courante. 
                    La participation financière du bénéficiaire est définie par le Conseil départemental.
                    Cette aide n’est pas cumulable avec l’Allocation compensatrice pour tierce personne (ACTP), la Majoration Tierce Personne (MTP versée par la CPAM) et les prestations d’aide-ménagère servies par les caisses de retraite
                    """

    def formula_2020_01(individu, period, parameters):
        taux_incapacite = individu('taux_incapacite', period)
        restriction_substantielle_durable = individu('aah_restriction_substantielle_durable_acces_emploi', period)
        age = individu('age', period)
        ressortissant_eee = individu('ressortissant_eee', period)
        possede_actp = individu('beneficiaire_actp', period)
        possede_mtp = individu('mtp', period)

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
        parameters_chemin = parameters(
            period).departements.eure_et_loir.aide_menagere

        condition_taux_incapacite = ((taux_incapacite >= parameters_chemin.taux_incapacite_superieur)
                                     + ((taux_incapacite < parameters_chemin.taux_incapacite_maximum_restriction_acces_emploi) *
                                        ((taux_incapacite > parameters_chemin.taux_incapacite_minimum_restriction_acces_emploi) * restriction_substantielle_durable)))
        condition_age = (age <= parameters_chemin.age_minimal_personne_handicap)
        condition_nationalite = ressortissant_eee + individu('refugie', period) + individu('apatride', period)
        # condition non intégrée : Les personnes de nationalité étrangère doivent justifier d'une résidence
        # en France métropolitaine ininterrompue depuis au moins 15 ans, et ce avant l'âge de 70 ans.
        condition_ressources = individu_resources <= individu.famille('aspa', period)
        condition_aides_actp = not_(possede_actp)
        condition_aides_mtp = not_(possede_mtp)
        condition_aide_menagere_caisse_retraite = not_(individu('aide_menagere_fournie_caisse_retraite', period))
        conditions_aides = condition_aide_menagere_caisse_retraite * condition_aides_actp * condition_aides_mtp

        return condition_residence * condition_taux_incapacite * condition_age * condition_nationalite * condition_ressources * conditions_aides
