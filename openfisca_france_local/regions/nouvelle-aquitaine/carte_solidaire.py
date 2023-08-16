 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, FoyerFiscal, Individu, MONTH, YEAR
from openfisca_france.model.caracteristiques_socio_demographiques.logement\
    import TypesCodeInseeRegion


class nouvelle_aquitaine_carte_solidaire_quotient_familial(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR
    label = u"Quotient familial pour la carte solidaire pour les transports de la Nouvelle Aquitaine"

    def formula(foyer_fiscal, period):
        return foyer_fiscal('rfr', period) /foyer_fiscal('nbptr', period)


class nouvelle_aquitaine_carte_solidaire_eligibilite_financiere(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = u"Éligibilité à la carte solidaire pour les transports de la Nouvelle Aquitaine"

    def formula(individu, period, parameters):
        qf = individu.foyer_fiscal('nouvelle_aquitaine_carte_solidaire_quotient_familial', period.n_2)
        b_aah = individu('aah', period) > 0
        b_ada = individu.famille('ada', period) > 0
        plafond = parameters(period).regions.nouvelle_aquitaine.carte_solidaire.plafond

        return ((qf < plafond) + b_aah + b_ada)


class nouvelle_aquitaine_carte_solidaire_eligibilite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité à la carte solidaire pour les transports de la Nouvelle Aquitaine"

    def formula(individu, period):
        region = individu.menage('region', period)
        nouvelle_aquitaine_eligibilite_residence = (
            region == TypesCodeInseeRegion.nouvelle_aquitaine)

        fin = individu(
            'nouvelle_aquitaine_carte_solidaire_eligibilite_financiere', period)
        return nouvelle_aquitaine_eligibilite_residence * fin


class nouvelle_aquitaine_carte_solidaire(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Réduction obtenue en \% avec la carte solidaire pour les transports de la Nouvelle Aquitaine"

    def formula(individu, period, parameters):
        reduction = parameters(period).regions.nouvelle_aquitaine.carte_solidaire.reduction
        elig = individu('nouvelle_aquitaine_carte_solidaire_eligibilite', period)
        return elig * reduction
