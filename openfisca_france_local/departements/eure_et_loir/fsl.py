import numpy as np

from openfisca_france.model.base import Variable, Menage, MONTH, TypesStatutOccupationLogement


class eure_et_loir_eligibilite_fsl_acces_logement(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité au Fonds de solidarité pour le Logement (FSL) – Accès au logement pour les personnes précarisées"
    reference = ["Chapitre 2 du règlement intérieur des Fonds de Solidarité pour le Logement d'Eure-et-Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RI_FSL28_2020_valide_AD_16.12.2019.pdf"
                 ]
    documentation = """
                    Le FSL « accès au logement » est un dispositif d’aide à l’accès à un logement. 
                    A ce titre, une aide, sous forme de subvention ou de prêt remboursable, peut être accordée pour le dépôt de garantie, 
                    le 1er loyer, les frais d’agence, la garantie de loyers et de charges locatives, les dettes locatives en vue d’un relogement par le même bailleur,
                     l’assurance habitation (6 premiers mois), les frais de déménagement, l’ouverture des compteurs, 
                     l’achat d’appareils ménagers et de mobilier de première nécessité.
                    """

    def formula_2020_01(menage, period):
        condition_residence = menage('eure_et_loir_eligibilite_residence', period)
        condition_ressources = menage('eure_et_loir_fsl_base_ressources', period)
        return condition_residence * condition_ressources


class eure_et_loir_fsl_eligibilite_installation_logement(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité au Fonds de solidarité pour le Logement (FSL) – Installation dans le logement pour les personnes précarisées"
    reference = ["Chapitre 2 du règlement intérieur des Fonds de Solidarité pour le Logement d'Eure-et-Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RI_FSL28_2020_valide_AD_16.12.2019.pdf"
                 ]
    documentation = """
                        Le FSL « installation dans le logement » est un dispositif qui destiné à favoriser l’installation des personnes défavorisées dans le cadre d’un premier accès au logement sur le département.
                        Il s’agit d’un aide pour des équipements de première nécessité.
                    """

    def formula_2020_01(menage, period):
        condition_residence = menage('eure_et_loir_eligibilite_residence', period)
        condition_ressources = menage('eure_et_loir_fsl_base_ressources', period)
        return condition_residence * condition_ressources


class eure_et_loir_fsl_eligibilite_maintien_logement(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité au Fonds de solidarité pour le Logement (FSL) – Maintien dans le logement pour les personnes précarisées"
    reference = ["Chapitre 2 du règlement intérieur des Fonds de Solidarité pour le Logement d'Eure-et-Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RI_FSL28_2020_valide_AD_16.12.2019.pdf"
                 ]
    documentation = """
                        Le FSL « maintien dans le logement » est un dispositif d’aide au maintien dans un logement. 
                        A ce titre, une aide, sous forme de subvention ou de prêt remboursable, peut être accordée pour la mise en jeu du cautionnement,
                         les impayés de loyer et le nettoyage et les petits travaux du logement.
                    """

    def formula_2020_01(menage, period):
        statut_occupation_logement = menage('statut_occupation_logement', period)

        condition_locataire_proprietaire = (       statut_occupation_logement == TypesStatutOccupationLogement.proprietaire) + (
                                                   statut_occupation_logement == TypesStatutOccupationLogement.locataire_hlm) + (
                                                   statut_occupation_logement == TypesStatutOccupationLogement.locataire_vide) + (
                                                   statut_occupation_logement == TypesStatutOccupationLogement.locataire_meuble) + (
                                                   statut_occupation_logement == TypesStatutOccupationLogement.locataire_foyer)
        condition_residence = menage('eure_et_loir_eligibilite_residence', period)
        condition_ressources = menage('eure_et_loir_fsl_base_ressources', period)

        return condition_residence * condition_locataire_proprietaire * condition_ressources


class eure_et_loir_fsl_eligibilite_maintien_fourniture(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité au Fonds de solidarité pour le Logement (FSL) – Maintien des fournitures  « Energie-Eau-Téléphone » pour les personnes précarisées"
    reference = ["Chapitre 2 du règlement intérieur des Fonds de Solidarité pour le Logement d'Eure-et-Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RI_FSL28_2020_valide_AD_16.12.2019.pdf"
                 ]
    documentation = """
                        Le FSL « Energie-Eau-Téléphone » est un dispositif d’aide visant à maintenir les flux afin que le ménage soit en mesure de vivre décemment dans son logement. 
                        A ce titre, une aide peut être accordée et versée au créancier.
                    """

    def formula_2020_01(menage, period, parameters):
        statut_occupation_logement = menage('statut_occupation_logement', period)
        condition_locataire_proprietaire = (statut_occupation_logement == TypesStatutOccupationLogement.proprietaire) + (
                                            statut_occupation_logement == TypesStatutOccupationLogement.locataire_hlm) + (
                                            statut_occupation_logement == TypesStatutOccupationLogement.locataire_vide) + (
                                            statut_occupation_logement == TypesStatutOccupationLogement.locataire_meuble) + (
                                            statut_occupation_logement == TypesStatutOccupationLogement.locataire_foyer)
        condition_residence = menage('eure_et_loir_eligibilite_residence', period)
        condition_ressources = menage('eure_et_loir_fsl_base_ressources', period)

        return condition_residence * condition_locataire_proprietaire * condition_ressources


class eure_et_loir_fsl_base_ressources(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Base de ressources prises en compte pour l'éligibilité au Fonds de solidarité pour le Logement (FSL)"
    reference = [
        "Annexe 1 du règlement intérieur des Fonds de Solidarité pour le Logement d'Eure-et-Loir",
        "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RI_FSL28_2020_valide_AD_16.12.2019.pdf"
    ]

    def formula_2020_01(menage, period, parameters):

        menage_resource_names = {
            'salaire_imposable',
            'chomage_imposable',
            'revenus_stage_formation_pro',
            'rsa_base_ressources_patrimoine_individu',
            'indemnites_journalieres',
            'pensions_alimentaires_percues',
            'prestation_compensatoire',
            'retraite_imposable',
            'aah',
            'pensions_invalidite',
            'apa_domicile',
            'pch'
        }

        menage_resources_annuelle_names = {
            'retraite_complementaire_artisan_commercant',
            'retraite_complementaire_profession_liberale'
        }
        menage_resource_names_famille = {
            'asf',
            'paje',
            'paje_cmg',
            'aeeh',
            'aide_logement',
            'aspa',
            'ppa',
            'bourse_college',
            'bourse_lycee'
        }
        menage_resource_names_famille_annuelles = {
            'ars'
        }
        menage_resources_mensuelles = np.sum(
            sum([menage.members(resource, period) for resource in menage_resource_names]))
        menage_resources_annuelles = np.sum(
            sum([menage.members(resource, period.this_year) for resource in menage_resources_annuelle_names]))
        menage_resources_mensuelles_famille = np.sum(
            sum([menage.members.famille(resource, period) for resource in menage_resource_names_famille]))
        menage_resources_annuelles_famille = np.sum(
            sum([menage.members.famille(resource, period.this_year) for resource in
                 menage_resource_names_famille_annuelles]))

        menage_resources = menage_resources_mensuelles + menage_resources_annuelles + menage_resources_mensuelles_famille + menage_resources_annuelles_famille
        nbenf = menage.members('enfant_a_charge', period.this_year)
        nb_enf_charge = int(menage.sum(nbenf))
        is_en_couple = menage.members.famille('en_couple', period)
        fsl_parameters = parameters(period).departements.eure_et_loir.fsl.fsl
        if is_en_couple[0]:
            seuil_pauvrete = fsl_parameters["en_" + str(nb_enf_charge)].couple
        else:
            seuil_pauvrete = fsl_parameters["en_" + str(nb_enf_charge)].single
        condition_ressources = True if menage_resources <= seuil_pauvrete else False
        return condition_ressources
