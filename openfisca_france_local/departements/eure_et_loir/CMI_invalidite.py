# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH
from openfisca_france.model.prestations.autonomie import TypesGir


class eure_et_loir_cmi_invalidite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité à la Carte mobilité inclusion invalididté"
    reference = """ Titre 4 Chapitre 1 du Règlement départemental d'Aide Sociale PA PH de l'Eure-et-Loir
                    Cette carte permet d’obtenir une priorité d’accès aux places assises dans les lieux publics, les salles d’attente et les transports en commun, de bénéficier d’avantages fiscaux et de réductions tarifaires.
                    Pour les bénéficiaires de l’Allocation personnalisée d’autonomie (APA), l’éligibilité de l’aide dépend niveau de GIR (1 ou 2).
                """

    def formula(individu, period,parameters):
        taux_incapacite = individu('taux_incapacite',period)
        beneficiaire_apa = individu('apa_domicile',period) # où apa_domicile est le montant de l'aide apa versé
        gir = individu('gir', period)

        condition_incapacite = (taux_incapacite >= parameters(period).departements.eure_et_loir.CMI_invalidite.taux_incapacite_minimal)
        condition_apa = 1 if beneficiaire_apa else 0
        condition_gir = ((gir == TypesGir.gir_1) or (gir == TypesGir.gir_2))

        conditions = condition_incapacite or (condition_gir and condition_apa)

        return conditions