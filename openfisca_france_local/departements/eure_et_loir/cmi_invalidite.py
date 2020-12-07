# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH
from openfisca_france.model.prestations.autonomie import TypesGir


class eure_et_loir_eligibilite_cmi_invalidite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-loir, éligibilité à la Carte mobilité inclusion invalidité"
    reference = [" Titre 4 Chapitre 1 du Règlement départemental d'Aide Sociale PA PH de l'Eure-et-Loir",
                 "https://github.com/openfisca/openfisca-france-local/wiki/files/departements/eure-et-loir/Fiche_15_CMI_Mention_Invalidite.pdf"]
    documentation = """
                    Cette carte permet d’obtenir une priorité d’accès aux places assises dans les lieux publics, les salles d’attente et les transports en commun, de bénéficier d’avantages fiscaux et de réductions tarifaires.
                    Pour les bénéficiaires de l’Allocation personnalisée d’autonomie (APA), l’éligibilité de l’aide dépend niveau de GIR (1 ou 2).
                    """

    def formula_2020_01(individu, period, parameters):
        taux_incapacite = individu('taux_incapacite', period)
        beneficiaire_apa = individu('apa_domicile', period)  # où apa_domicile est le montant de l'aide apa versé
        gir = individu('gir', period)
        nationalite = individu('ressortissant_eee', period) + individu('titre_sejour', period) + individu('refugie',period) + individu('apatride', period)

        parameters_chemin = parameters(
            period).departements.eure_et_loir.transports
        condition_nationalite = nationalite
        condition_residence = individu.menage('eure_et_loir_eligibilite_residence', period)
        condition_incapacite = (taux_incapacite >= parameters_chemin.cmi_invalidite.taux_incapacite_minimal)
        condition_apa = 1 if beneficiaire_apa else 0
        condition_gir = ((gir == TypesGir.gir_1) + (gir == TypesGir.gir_2))
        conditions = condition_nationalite * condition_residence * (condition_incapacite + (condition_gir * condition_apa))

        return conditions