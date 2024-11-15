 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Famille, Menage, MONTH, Variable, select

class antony_aide_depart_sejour_adapte(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Montant total de l'Aide au départ en séjour adapté de la ville de Antony"
    reference = "https://www.ville-antony.fr/aide-aux-departs-en-sejours-vacances"

    def formula(famille, period, parameters):
        residence_antony = famille.demandeur.menage('antony_eligibilite_residence', period)

        condition_ressources_remplies = famille('antony_eligibilite_ressources', period)

        nb_enfants_handicapes = famille.sum(famille.members('handicap', period), role = Famille.ENFANT)
        montant_individuel = famille('antony_aide_depart_sejour_adapte_montant_individuel', period)
        montant_total = montant_individuel * nb_enfants_handicapes

        return residence_antony * condition_ressources_remplies * montant_total


class antony_aide_depart_sejour_adapte_montant_individuel(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Montant de base applicable à chaque individu pour l'Aide au départ en séjour adapté de la ville de Antony"

    def formula(famille, period, parameters):
        parameters_antony = parameters(period).communes.antony.plafonds_revenus.sejour_adapte

        # Les plafonds sont mensuels et les ressources sont considérées sur 3 mois
        # On remet donc les ressources à un niveau mensuel pour la comparaison
        ressources_considerees_famille = famille('antony_base_ressources', period) / 3

        montant = select(
            [
                ressources_considerees_famille < parameters_antony.tranches.tranche_1,
                ressources_considerees_famille < parameters_antony.tranches.tranche_2
            ],
            [
                parameters_antony.montants.montant_tranche_1,
                parameters_antony.montants.montant_tranche_2
            ],
            default=0
        )

        return montant
