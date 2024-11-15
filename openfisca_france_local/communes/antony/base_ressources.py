 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore


class antony_base_ressources(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Base ressources d'une famille aux dispositifs d'Antony"

    def formula(famille, period, parameters):
        # M-1 to M-3
        last_three_months = period.last_3_months

        ressources_individus_a_inclure = [
            'salaire_imposable',
            'retraite_imposable',
            'chomage_imposable',
            'pensions_invalidite',
            'indemnites_journalieres',
            'aah',
            'pensions_alimentaires_percues'
        ]

        ressources_famille_a_inclure = [
            'af',
            'cf',
            'paje',
            'asf',
            'aeeh',
            'rsa',
            'ppa'
        ]

        resources_mensuelles_individus_m_3 = sum([
            famille.members(resource, last_three_months, options=[ADD])
            for resource in ressources_individus_a_inclure
        ])
        ressources_mensuelles_famille_m_3 = sum([
            famille(resource, last_three_months, options=[ADD])
            for resource in ressources_famille_a_inclure
        ])
        ressources_m_3 = ressources_mensuelles_famille_m_3 + famille.sum(resources_mensuelles_individus_m_3)

        rfr_equivalent_m_3 = famille.demandeur.foyer_fiscal('rfr', period.n_2) / 4

        ressources_considerees = select(
            [((ressources_m_3 > 0) * (rfr_equivalent_m_3 > 0)), (ressources_m_3 > 0), (rfr_equivalent_m_3 > 0)],
            [min_(ressources_m_3, rfr_equivalent_m_3), ressources_m_3, rfr_equivalent_m_3],
            default=0
        )

        return ressources_considerees


class antony_eligibilite_ressources(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH
    label = "Éligibilité de ressources d'une famille aux dispositifs d'Antony"

    def formula(famille, period, parameters):
        parameters_antony = parameters(period).communes.antony.plafonds_revenus
        baremes_enfants = parameters_antony.bareme_enfants.bareme_ressources_par_enfant

        ressources_considerees = famille('antony_base_ressources', period)

        nb_enfants = famille.nb_persons(role=Famille.ENFANT)

        en_couple = famille('en_couple', period)

        plafond_considere = select(
            [not_(en_couple) * (nb_enfants == 0), en_couple * (nb_enfants == 0), nb_enfants > 0],
            # Le barème ne va que jusqu'à 7 enfants, on considère donc 7 enfants au plus dans le calcule du barème
            # avec min_(nb_enfants, 7)
            [parameters_antony.personne_seule, parameters_antony.couple, baremes_enfants.calc(min_(nb_enfants, 7))]
        )

        # Les plafonds sont mensuels et les ressources sont considérées sur 3 mois
        # On remet donc les ressources à un niveau mensuel pour la comparaison
        return (ressources_considerees / 3) < plafond_considere
