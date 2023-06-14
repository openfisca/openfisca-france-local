from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select, where, logical_or as or_, round as round_)


from openfisca_core.periods import Period

from openfisca_france.model.base import *  # noqa analysis:ignore

from openfisca_france_local.metropoles.rennes.communes import communes


class residence_rennes_metropole(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = u"Le lieu de résidence se situe dans une commune faisant partie de Rennes Métropole"

    def formula(individu, period):
        code_insee_commune = individu.menage('depcom', period)
        return sum([code_insee_commune == code_insee for code_insee in communes])


class rennes_metropole_transport_base_ressource(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Base ressources pour la tarification solidaire de Rennes Métropole"

    def formula(individu, period, parameters):
        # pensions_alimentaires_versees

        # renvenus BIC ou B
        def revenus_tns():
            revenus_auto_entrepreneur = individu('rpns_auto_entrepreneur_benefice', period.last_3_months, options = [ADD])

            # Les revenus TNS hors AE sont estimés en se basant sur le revenu N-1
            rpns_micro_entreprise_benefice = individu('rpns_micro_entreprise_benefice', period.last_year, options = [ADD])
            rpns_benefice_exploitant_agricole = individu('rpns_benefice_exploitant_agricole', period.last_year, options = [ADD])
            rpns_autres_revenus = individu('rpns_autres_revenus', period.last_year, options = [ADD])
            return (revenus_auto_entrepreneur + rpns_micro_entreprise_benefice + rpns_benefice_exploitant_agricole + rpns_autres_revenus) * (3 / 12)

        # on prend en compte le salaire du conjoint
        last_year = Period(('year', period.start, 1)).offset(-1)

        ressources_individuelles_annuelles = (
            individu('aah', last_year, options = [ADD])
            + individu('ass', last_year, options = [ADD])
            + individu('chomage_net', last_year, options = [ADD])
            + individu('indemnites_journalieres', last_year, options = [ADD])
            + individu('pensions_alimentaires_percues', last_year, options = [ADD])
            + individu('pensions_invalidite', last_year, options = [ADD])
            + individu('retraite_combattant', last_year, options = [ADD])
            + individu('retraite_nette', last_year, options = [ADD])
            + individu('revenus_stage_formation_pro', last_year, options = [ADD])
            + individu('revenus_capital', last_year, options = [ADD])
            + individu('revenus_locatifs', last_year, options = [ADD])
            + individu('salaire_net', last_year, options = [ADD])
            + revenus_tns()
            - individu('pensions_alimentaires_versees_individu', period.last_3_months, options = [ADD])
            )

        ressources_familiales_annuelles = (
            individu.famille('af', last_year, options = [ADD])
            + round_(individu.famille('rsa', last_year, options = [ADD]))
            + individu.famille('aide_logement', last_year, options = [ADD])
            + individu.famille('asf', last_year, options = [ADD])
            + individu.famille('aspa', last_year, options = [ADD])
            + individu.famille('cf', last_year, options = [ADD])
            + individu.famille('paje_base', last_year, options = [ADD])
            + individu.famille('paje_clca', last_year, options = [ADD])
            + individu.famille('paje_prepare', last_year, options = [ADD])
            + individu.famille('ppa', last_year, options = [ADD])
            )

        ressources_familiales = (ressources_familiales_annuelles + individu.famille.sum(ressources_individuelles_annuelles)) / 12

        forfait_logement = individu.famille('css_cmu_forfait_logement_al', period) / 12
        aide_logement = individu.famille('aide_logement', last_year, options = [ADD]) / 12
        rsa = round_(individu.famille('rsa', last_year, options = [ADD]) / 12)
        touche_que_aah = ressources_familiales - aide_logement - (individu.famille.sum(individu('aah', last_year, options = [ADD])) / 12) - rsa
        forfait_aah = where(touche_que_aah, '0', '1')
        ressources_familiales = where(forfait_aah, ressources_familiales - aide_logement + forfait_logement, ressources_familiales)

        touche_que_aspa = ressources_familiales - aide_logement - (individu.famille('aspa', last_year, options = [ADD]) / 12) - rsa
        forfait_aspa = where(touche_que_aspa, '0', '1')
        ressources_familiales = where(forfait_aspa, ressources_familiales - aide_logement + forfait_logement, ressources_familiales)

        return ressources_familiales


class rennes_metropole_transport(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Calcul tarification solidaire"

    def formula(individu, period, parameters):
        nombre_enfants = individu.famille('af_nbenf', period)
        ressources_familiales = individu('rennes_metropole_transport_base_ressource', period)
        # montant_par_enfant = simulation.legislation_at(period.start).metropoles.rennes.mon_aide.montant

        seuil1 = parameters(period.start).metropoles.rennes.tarification_solidaire.seuil.seuil1
        seuil2 = parameters(period.start).metropoles.rennes.tarification_solidaire.seuil.seuil2
        seuil3 = parameters(period.start).metropoles.rennes.tarification_solidaire.seuil.seuil3

        taux1 = parameters(period.start).metropoles.rennes.tarification_solidaire.taux_reduction.taux1
        taux2 = parameters(period.start).metropoles.rennes.tarification_solidaire.taux_reduction.taux2
        taux3 = parameters(period.start).metropoles.rennes.tarification_solidaire.taux_reduction.taux3

        # determine si une personne seule a des enfants qui est considéré de fait comme un couple
        individu_en_couple = or_(individu.famille('en_couple', period), nombre_enfants >= 1)

        # salaire =  simulation.compute('salaire_net', period)
       # salaire_cumul = self.sum_by_entity(salaire, entity = 'famille')

        # ----------------------on retire les apl et on ajoute le forfait logement si ahh seul revenu---------------------------

        seuil_evolutif = (1 + individu_en_couple * (0.5 + nombre_enfants * 0.3))

        result_non_etudiant = select([ressources_familiales <= seuil1 * seuil_evolutif, ressources_familiales <= seuil2 * seuil_evolutif, ressources_familiales <= seuil3 * seuil_evolutif], [taux1, taux2, taux3])

        etudiant = individu('etudiant', period)
        echelon = individu('bourse_criteres_sociaux_echelon', period)
        result_etudiant = select([echelon >= 5, echelon >= 3, echelon >= 2], [taux1, taux2, taux3])
        result = where(etudiant, result_etudiant, result_non_etudiant)

        residence_rennes_metropole = individu('residence_rennes_metropole', period)

        return result * residence_rennes_metropole
