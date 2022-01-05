 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, MONTH, select, TypesActivite

class tisseo_transport_invalide_reduction(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Pourcentage de la réduction pour les personnes en situation de handicap"

    def formula(individu, period, parameters):
        taux_incapacite = individu('taux_incapacite', period)
        ressources = individu.foyer_fiscal('tisseo_transport_reduction_ressources_fiscales', period.n_2)

        aah = parameters(period).prestations_sociales.prestations_etat_de_sante.invalidite.aah.montant
        smic_net_mensuel = individu('tisseo_transport_reduction_plafond_smic_net', period)

        reduction_50_80 = select([
            ressources <= aah,
            ressources <= smic_net_mensuel
            ], [100, 80], default=70)
        return select([
            taux_incapacite < 0.50,
            taux_incapacite < 0.80,
            ], [
            0,
            reduction_50_80,
            ], default=100)
