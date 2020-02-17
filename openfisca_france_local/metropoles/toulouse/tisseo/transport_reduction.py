 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, FoyerFiscal, Individu, MONTH, YEAR, max_

class tisseo_transport_reduction(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Pourcentage de la réduction pour les abonnements sur le réseau Tisséo de la métropole de Toulouse"

    def formula(individu, period):
        ressort_territorial = individu.menage('tisseo_ressort_territorial', period)

        jeune = max_(
          individu('tisseo_transport_jeune_reduction', period),
          individu('tisseo_transport_etudiant_reduction', period)
          )

        demandeur_emploi = max_(
          individu('tisseo_transport_demandeur_emploi_indemnise_reduction', period),
          individu('tisseo_transport_demandeur_emploi_non_indemnise_reduction', period)
          )

        retraite_invalide = max_(
          individu('tisseo_transport_retraite_reduction', period),
          individu('tisseo_transport_invalide_reduction', period)
          )

        reduction_maximum = max_(max_(jeune, demandeur_emploi), retraite_invalide)
        return ressort_territorial * reduction_maximum
