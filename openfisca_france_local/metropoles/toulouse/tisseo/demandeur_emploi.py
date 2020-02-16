 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH, TypesActivite, select

class tisseo_transport_demandeur_emploi_indemnise_reduction(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Pourcentage de la réduction pour les demandeurs d'emploi indemnisés"

    def formula(individu, period, parameters):
        chomage_net = individu('chomage_net', period.last_month)
        indemnise = chomage_net > 0
        smic_net = individu('tisseo_transport_reduction_plafond_smic_net', period)

        cmu_c_plafond = individu.famille('cmu_c_plafond', period) / 12
        return indemnise * select([
            chomage_net <= cmu_c_plafond,
            chomage_net <= smic_net
            ], [100, 80], default=70)


class tisseo_transport_demandeur_emploi_non_indemnise_reduction(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Pourcentage de la réduction pour les demandeurs d'emploi non indemnisés"

    def formula(individu, period, parameters):
        chomeur = individu('activite', period) == TypesActivite.chomeur

        ressources = individu.foyer_fiscal('tisseo_transport_reduction_ressources_fiscales', period.n_2)
        smic_net = individu('tisseo_transport_reduction_plafond_smic_net', period)

        return chomeur * (ressources <= smic_net) * 80
