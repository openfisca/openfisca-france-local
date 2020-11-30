# -*- coding: utf-8 -*-
# from openfisca_france.model.base import Variable, Menage, YEAR
from openfisca_france.model.base import Variable, Menage, MONTH, not_, YEAR, Individu
from openfisca_core import reforms
from numpy.core.defchararray import startswith
from openfisca_france_local.fsl_factory import *

class eure_et_loir_fsl_acces_logement(Variable):
    value_type = bool
    entity = Individu
    definition_period = YEAR
    label = "Éligibilité au Fonds de solidarité pour le logement (FSL) – Accès au logement pour les personnes précarisées"
    reference = """Chapitre 2 du règlement intérieur des Fonds de Solidarité pour le logement d'Eure-et-Loir
                    Le FSL « accès au logement » est un dispositif d’aide à l’accès à un logement. 
                    A ce titre, une aide, sous forme de subvention ou de prêt remboursable, peut être accordée pour le dépôt de garantie, 
                    le 1er loyer, les frais d’agence, la garantie de loyers et de charges locatives, les dettes locatives en vue d’un relogement par le même bailleur,
                     l’assurance habitation (6 premiers mois), les frais de déménagement, l’ouverture des compteurs, 
                     l’achat d’appareils ménagers et de mobilier de première nécessité.
                """

    def formula_2020(menage, period, parameters):
        menage_resource_names = {
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

        menage_resources = sum([individu.menage(resource, period.first_month) for resource in menage_resource_names])
        type_menage = individu.menage('type_menage', period.first_month)
        af_nbenf = individu.menage.personne_de_reference.famille('af_nbenf', period.first_month)
        isole = not (individu.menage.personne_de_reference.famille('en_couple', period.first_month))

        seuil_pauvrete = 1600
        if not(isole) :
            seuil_pauvrete = parameters(
                                 period).departements.eure_et_loir.fsl.couple_enfant[af_nbenf]
        else:
            seuil_pauvrete = parameters(
                                 period).departements.eure_et_loir.fsl.mono_enfant[af_nbenf]

        condition_ressources = 1 if menage_resources <= seuil_pauvrete else 0
        return condition_ressources
#




# class eure_et_loir_fsl_installation_logement(Variable):
#     value_type = bool
#     entity = Menage
#     definition_period = YEAR
#     label = "Éligibilité au Fonds de solidarité pour le logement (FSL) – Installation dans le logement pour les personnes précarisées"
#     reference = """Chapitre 2 du règlement intérieur des Fonds de Solidarité pour le logement d'Eure-et-Loir
#                     Le FSL « installation dans le logement » est un dispositif qui destiné à favoriser l’installation des personnes défavorisées dans le cadre d’un premier accès au logement sur le département.
#                     Il s’agit d’un aide pour des équipements de première nécessité.
#                 """
#
#     def formula(menage, period):
#         menage_resource_names = {
#             'ass',
#             'chomage_net',
#             'retraite_nette',
#             'salaire_net',
#             'allocation_securisation_professionnelle',
#             'dedommagement_victime_amiante',
#             'gains_exceptionnels',
#             'indemnites_chomage_partiel',
#             'indemnites_journalieres',
#             'indemnites_volontariat',
#             'pensions_invalidite',
#             'prestation_compensatoire',
#             'prime_forfaitaire_mensuelle_reprise_activite',
#             'retraite_brute',
#             'revenus_stage_formation_pro',
#             'rsa_base_ressources_patrimoine_individu'
#         }
#
#         menage_resources = sum([menage(resource, period.last_month) for resource in menage_resource_names])
#         type_menage = menage('type_menage', period)
#
#         af_nbenf = menage.personne_de_reference.famille('af_nbenf', period.first_month)
#         isole = not (menage.personne_de_reference.famille('en_couple', period.first_month))
#
#         seuil_pauvrete = eure_et_loir_retourne_seuil(type_menage, af_nbenf, isole)
#
#         condition_ressources = 1 if menage_resources <= seuil_pauvrete else 0
#
#         return condition_ressources


