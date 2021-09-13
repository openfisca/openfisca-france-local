# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH, not_


class eure_et_loir_eligibilite_pch_domicile(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité d'une personne en situation de handicap à la prestation de compensation de handicap à domicile"
    reference = ["Titre 3 Chapitre 1-3 du Règlement départemental d'Aide Sociale PA PH de l'Eure et Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RDAS_valide__decembre_2019.pdf"
                 ]
    documentation = """
                   La Prestation de compensation du handicap à domicile (PCH) a pour but de compenser les conséquences du handicap. C’est une aide personnalisée, modulable en fonction des besoins de chaque bénéficiaire. Elle peut financer des aides humaines, des aides techniques, des aides pour l’aménagement du logement et/ou du véhicule, les surcoûts liés au transport, des aides animalières, des charges spécifiques (service de téléalarme, etc.) ou exceptionnelles. 
                   Cette aide n’est pas cumulable avec l’Allocation compensatrice pour tierce personne (ACTP), l’Allocation personnalisée d’autonomie (APA) et l’Allocation d’éducation de l’enfant handicapé (AEEH)
                   L’attribution de l’aide est soumise à une évaluation de la situation du demandeur par la Maison départementale de l’autonomie (MDA).
                    """

    def formula_2020_01(individu, period):
        condition_residence = individu.menage('eure_et_loir_eligibilite_residence', period)
        condition_nationalite = individu('ressortissant_eee', period)+ individu('titre_sejour', period) + individu('refugie',period) + individu('apatride',period)
        condition_handicap = individu('handicap', period)
        condition_aides_aeeh = not_(individu.famille('beneficiaire_complement_aeeh', period))
        condition_aides_apa =  not_(individu('apa_domicile', period) > 0)
        conditions_aides_actp_acfp = not_(individu('beneficiaire_actp', period)) * not_(individu('beneficiaire_acfp',period))

        return condition_residence * condition_nationalite * condition_handicap * condition_aides_aeeh * condition_aides_apa * conditions_aides_actp_acfp


class eure_et_loir_eligibilite_pch_etablissement(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Loir,éligibilité d'une personne en situation de handicap à la prestation de compensation de handicap en établissement"
    reference = ["Titre 3 Chapitre 2-2 du Règlement départemental d'Aide Sociale PA PH de l'Eure et Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RDAS_valide__decembre_2019.pdf"
                 ]
    documentation = """
                   La PCH en établissement a pour but de compenser les conséquences du handicap durant les périodes d’interruption d’hospitalisation ou d’hébergement en établissement. C’est une aide personnalisée, modulable en fonction des besoins de chaque bénéficiaire. Elle peut financer des aides humaines, des aides techniques, des aides pour l’aménagement du logement et/ou du véhicule, les surcoûts liés au transport, etc.
                   Cette aide n’est pas cumulable avec l’Allocation compensatrice pour tierce personne (ACTP), l’Allocation personnalisée d’autonomie (APA) et l’Allocation d’éducation de l’enfant handicapé (AEEH)
                   L’attribution de l’aide est soumise à une évaluation de la situation du demandeur par la Maison départementale de l’autonomie (MDA).
                    """

    def formula_2020_01(individu, period):
        condition_residence = individu.menage('eure_et_loir_eligibilite_residence', period)
        condition_nationalite = individu('ressortissant_eee', period) + individu('titre_sejour', period) + individu('refugie',period) + individu('apatride',period)
        condition_handicap = individu('handicap', period)
        condition_hebergement = individu.famille('place_hebergement', period)

        condition_aides_aeeh = not_(individu.famille('beneficiaire_complement_aeeh', period))
        condition_aides_apa = not_(individu('apa_domicile', period) > 0)
        conditions_aides_actp_acfp = not_(individu('beneficiaire_actp', period)) * not_(individu('beneficiaire_acfp', period))

        return condition_residence * condition_nationalite * condition_handicap * condition_hebergement * condition_aides_aeeh * condition_aides_apa * conditions_aides_actp_acfp
