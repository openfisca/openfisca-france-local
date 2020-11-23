# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, Menage, MONTH


class eure_et_loir_PCH_domicile(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité d'une personne en situation de handicap à la prestation de compensation de handicap à domicile"
    reference = """Titre 3 Chapitre 1-3 du Règlement départemental d'Aide Sociale PA PH de l'Eure et Loir
                   La Prestation de compensation du handicap à domicile (PCH) a pour but de compenser les conséquences du handicap. C’est une aide personnalisée, modulable en fonction des besoins de chaque bénéficiaire. Elle peut financer des aides humaines, des aides techniques, des aides pour l’aménagement du logement et/ou du véhicule, les surcoûts liés au transport, des aides animalières, des charges spécifiques (service de téléalarme, etc.) ou exceptionnelles. 
                   Cette aide n’est pas cumulable avec l’Allocation compensatrice pour tierce personne (ACTP), l’Allocation personnalisée d’autonomie (APA) et l’Allocation d’éducation de l’enfant handicapé (AEEH)
                   L’attribution de l’aide est soumise à une évaluation de la situation du demandeur par la Maison départementale de l’autonomie (MDA).
                """

    def formula_2020_01(individu, period):
        ressortissant_eee = individu('ressortissant_eee', period)
        situation_handicap = individu('handicap', period)
        possede_aeeh = individu.famille('aeeh', period)
        possede_apa = individu('apa_domicile', period)
        possede_actp = individu('actp',period)

        condition_nationalite = ressortissant_eee if ressortissant_eee else individu('titre_sejour', period)
        condition_handicap = situation_handicap
        condition_aides_aeeh = 0 if possede_aeeh else 1
        condition_aides_apa = 0 if possede_apa else 1
        condition_aides_actp = 0 if possede_actp else 1

        return condition_nationalite * condition_handicap * condition_aides_aeeh * condition_aides_apa * condition_aides_actp


class eure_et_loir_PCH_etablissement(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité d'une personne en situation de handicap à la prestation de compensation de handicap en établissement"
    reference = """Titre 3 Chapitre 2-2 du Règlement départemental d'Aide Sociale PA PH de l'Eure et Loir
                   La PCH en établissement a pour but de compenser les conséquences du handicap durant les périodes d’interruption d’hospitalisation ou d’hébergement en établissement. C’est une aide personnalisée, modulable en fonction des besoins de chaque bénéficiaire. Elle peut financer des aides humaines, des aides techniques, des aides pour l’aménagement du logement et/ou du véhicule, les surcoûts liés au transport, etc.
                   Cette aide n’est pas cumulable avec l’Allocation compensatrice pour tierce personne (ACTP), l’Allocation personnalisée d’autonomie (APA) et l’Allocation d’éducation de l’enfant handicapé (AEEH)
                   L’attribution de l’aide est soumise à une évaluation de la situation du demandeur par la Maison départementale de l’autonomie (MDA).
                """

    def formula_2020_01(individu, period):
        ressortissant_eee = individu('ressortissant_eee', period)

        condition_nationalite = ressortissant_eee if ressortissant_eee else individu('titre_sejour', period)
        condition_handicap = individu('handicap', period)
        condition_hebergement = individu.famille('place_hebergement', period)

        return condition_nationalite * condition_handicap * condition_hebergement
