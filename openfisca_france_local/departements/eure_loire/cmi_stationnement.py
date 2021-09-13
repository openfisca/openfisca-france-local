# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH
from openfisca_france.model.prestations.autonomie import TypesGir

class eure_et_loir_eligibilite_cmi_stationnement(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Lor,éligibilité à la Carte mobilité inclusion stationnement"
    reference = [" Titre 4 Chapitre 1 du Règlement départemental d'Aide Sociale PA PH de l'Eure-et-Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/Fiche_15ter_CMI_Mention_Stationnement.pdf"
                 ]
    documentation = """
                        Cette carte donne droit au stationnement sur les places réservées aux personnes en situation de handicap sur le stationnement public.   
                    """

    def formula_2020_01(individu, period):
        gir = individu('gir', period)

        condition_nationalite = individu('ressortissant_eee', period) + individu('titre_sejour', period) + individu('refugie',period) + individu('apatride', period)
        condition_residence = individu.menage('eure_et_loir_eligibilite_residence', period)
        condition_apa = (individu('apa_domicile', period) > 0 ) # où apa_domicile est le montant de l'aide apa versé
        condition_gir = ((gir == TypesGir.gir_1) + (gir == TypesGir.gir_2))

        return condition_nationalite * condition_residence * condition_apa * condition_gir
