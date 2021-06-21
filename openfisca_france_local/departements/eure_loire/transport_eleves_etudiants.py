# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH

class eure_et_loir_eligibilite_transport_eleves_etudiants(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité à l'aide au Transport des élèves et étudiants en situation de handicap"
    reference = [" Titre 3 Chapitre 3 du Règlement départemental d'Aide Sociale PA PH de l'Eure-et-Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/RDAS_valide__decembre_2019.pdf"
                 ]
    documentation = """
                    Les frais de déplacement exposés par les élèves et étudiants en situation de handicap qui ne peuvent utiliser les moyens de transport en commun en raison de la gravité de leur handicap, médicalement établie, sont pris en charge par le Conseil départemental.
                    L’attribution de l’aide est soumise à une évaluation de la situation du demandeur par la Maison départementale de l’autonomie (MDA).
                    """

    def formula_2020_01(individu, period):
        etudiant = individu('etudiant', period) # regroupe les 2 activités : étudiant ET élève
        handicap = individu('handicap',period)
        condition_residence = individu.menage('eure_et_loir_eligibilite_residence', period)

        return condition_residence * etudiant * handicap
