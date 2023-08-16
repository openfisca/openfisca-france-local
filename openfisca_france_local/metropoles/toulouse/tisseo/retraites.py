 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH, select, TypesActivite

class tisseo_transport_retraite_reduction(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Pourcentage de la réduction pour les retraités"

    def formula(individu, period, parameters):
        retraite = individu('activite', period) == TypesActivite.retraite
        age = individu('age', period)

        ressources = individu.foyer_fiscal('tisseo_transport_reduction_ressources_fiscales', period.n_2)

        aah = parameters(period).prestations_sociales.prestations_etat_de_sante.invalidite.aah.montant
        smic_net_mensuel = individu('tisseo_transport_reduction_plafond_smic_net', period)
        return (retraite + (65 <= age)) * select([
            ressources <= aah,
            ressources <= smic_net_mensuel
            ], [100, 80], default=70)
