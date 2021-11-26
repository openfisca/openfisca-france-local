 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore


class antony_base_ressources(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Éligibilité de ressoures d'une aux dipositifs d'Antony"

    def formula(famille, period, parameters):
        # N-1
        last_year = period.last_year

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

        # This is a comment
        ressources_famille_annuelles_a_inclure = [
            'ars'
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

        resources_mensuelles_individus_n_1 = sum([
            famille.members(resource, last_year, options=[ADD])
            for resource in ressources_individus_a_inclure
        ])
        ressources_mensuelles_famille_n_1 = sum([
            famille(resource, last_year, options=[ADD])
            for resource in ressources_famille_a_inclure
        ])
        ressources_annuelles_famille_n_1 = sum([
            famille(resource, last_year)
            for resource in ressources_famille_annuelles_a_inclure
        ])
        ressources_n_1 = (famille.sum((resources_mensuelles_individus_n_1 / 4))
                          + (ressources_mensuelles_famille_n_1 / 4)
                          + (ressources_annuelles_famille_n_1 / 4)
                          )
        # on ne compare les ressources recentes avec le N-1
        # que si on a effectivement des ressources N-1
        ressources_considerees = where(ressources_n_1 > 0, min_(ressources_m_3, ressources_n_1), ressources_m_3)

        return ressources_considerees


class antony_eligibilite_ressources(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH
    label = "Éligibilité de ressoures d'une aux dipositifs d'Antony"

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

        return ressources_considerees < plafond_considere
