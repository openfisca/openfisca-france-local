 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore


class antony_aide_depart_sejour_adapte(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Montant total de l'Aide au depart en sejour adapté de la ville de Antony"

    def formula(famille, period, parameters):
        residence_antony = famille.demandeur.menage('antony_eligibilite_residence', period)

        condition_ressources_remplies = famille('antony_eligibilite_ressources', period)

        handicap = famille.members('handicap', period)
        montant_individuel = famille('antony_aide_depart_sejour_adapte_montant_individuel', period)
        montant_total = famille.sum(montant_individuel * handicap)

        return residence_antony * condition_ressources_remplies * montant_total


class antony_aide_depart_sejour_adapte_montant_individuel(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Montant de base applicable à chaque individu pour l'Aide au depart en sejour adapté de la ville de Antony"

    def formula(famille, period, parameters):
        parameters_antony = parameters(period).communes.antony.plafonds_revenus.sejour_adapte

        ressources_famille = famille('antony_base_ressources', period)

        montant = select(
            [
                ressources_famille < parameters_antony.tranches.tranche_1,
                ressources_famille < parameters_antony.tranches.tranche_2
            ],
            [
                parameters_antony.montants.montant_tranche_1,
                parameters_antony.montants.montant_tranche_2
            ],
            default=0
        )

        return montant
