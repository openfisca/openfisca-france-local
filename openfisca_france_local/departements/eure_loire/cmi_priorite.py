# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH

class eure_et_loir_eligibilite_cmi_priorite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-loir, éligibilité à la Carte mobilité inclusion priorité"
    reference = [" Titre 4 Chapitre 1 du Règlement départemental d'Aide Sociale PA PH de l'Eure-et-Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/Fiche_15_CMI_Mention_Invalidite.pdf"]
    documentation = """
                   Cette carte permet d’obtenir une priorité d’accès aux places assises dans les lieux publics, 
                   les salles d’attente et les transports en commun.
                    """

    def formula_2020_01(individu, period, parameters):

        parameters_chemin = parameters(period).departements.eure_et_loir.transports
        condition_residence = individu.menage('eure_et_loir_eligibilite_residence', period)
        conditions_taux_incapacite = individu('taux_incapacite', period) < parameters_chemin.taux_incapacite_minimal
        conditions_station_debout = individu('station_debout_penible',period)
        condition_nationalite = individu('ressortissant_eee',period) + individu('titre_sejour',period) + individu('refugie',period) + individu('apatride', period)

        return  condition_nationalite * condition_residence * conditions_taux_incapacite * conditions_station_debout
