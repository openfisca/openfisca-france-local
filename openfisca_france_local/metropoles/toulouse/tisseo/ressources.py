 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, FoyerFiscal, Individu, MONTH, YEAR

class tisseo_transport_reduction_ressources_fiscales(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR
    label = u"Base ressource fiscales pour les titres de transports Tisséo"

    def formula(foyer_fiscal, period):
        return foyer_fiscal('rfr', period) / foyer_fiscal('nbptr', period) / 12


class tisseo_transport_reduction_plafond_smic_net(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Base du SMIC net pour les titres de transports Tisséo"

    def formula(individu, period, parameters):
        smic = parameters(period).marche_travail.salaire_minimum.smic
        smic_brut_mensuel = smic.smic_b_horaire * smic.nb_heures_travail_mensuel

        # Utilisation des valeurs indicatives de service-public.fr pour passer du SMIC brut au SMIC net
        # https://www.service-public.fr/particuliers/vosdroits/F2300
        # Dans l'attente de la formule effectivement utilisée par la ville d'Alfortville
        return 7.82 / 9.88 * smic_brut_mensuel
