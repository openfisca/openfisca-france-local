from openfisca_france.model.base import *
import numpy as np


# strasbourg_sport_limitation_reduction
class sslr(Variable):
    label = "strasbourg_sport_limitation_reduction"
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        return 1000


class strasbourg_piscine_abonnement_annuel(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH


class strasbourg_piscine_abonnement_annuel_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        abo = individu("strasbourg_piscine_abonnement_annuel", period)

        reduit = individu("strasbourg_sports_reduit", period)

        bareme_qf = parameters(period).communes.strasbourg.piscine.abonnement_annuel.bareme
        bareme_qf_reduit = parameters(
            period
        ).communes.strasbourg.piscine.abonnement_annuel.bareme_reduit
        montant_reduit = bareme_qf_reduit.calc(qf)
        montant = bareme_qf.calc(qf)
        montant_qf = np.where(reduit, min_(montant_reduit, montant+individu('sslr', period)), montant)
        return abo * montant_qf


class strasbourg_piscine_abonnement_ce(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH


class strasbourg_piscine_abonnement_ce_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        abo = individu("strasbourg_piscine_abonnement_ce", period)
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme_qf = parameters(period).communes.strasbourg.piscine.ce.abonnement
        return abo * bareme_qf.calc(qf)


class strasbourg_piscine_abonnement_ete(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH


class strasbourg_piscine_abonnement_ete_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        abo = individu("strasbourg_piscine_abonnement_ete", period)
        bareme = parameters(period).communes.strasbourg.piscine.abonnement_ete
        return abo * bareme.calc(qf)


class strasbourg_sports_reduit(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        return (
            individu("ass", period)
            + individu.famille("rsa", period)
            + individu("evasion", period)
            + individu("cada", period)
            + individu("etudiant", period)
            + (individu("age", period) <= 18)
            + (individu("taux_incapacite", period) >= 0.8)
            + individu.famille("agent_ems", period)
        )


class strasbourg_piscine_entree_unitaire_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        age = individu("age", period.first_month)

        reduit = individu("strasbourg_sports_reduit", period)

        bareme_age = parameters(
            period
        ).communes.strasbourg.piscine.entree_unitaire.bareme_age
        bareme_qf = parameters(
            period
        ).communes.strasbourg.piscine.entree_unitaire.bareme_qf
        bareme_qf_reduit = parameters(
            period
        ).communes.strasbourg.piscine.entree_unitaire.bareme_qf_reduit
        montant_reduit = bareme_qf_reduit.calc(qf)
        montant = bareme_qf.calc(qf)
        montant_qf = np.where(reduit, min_(montant_reduit, montant+individu('sslr', period)), montant)
        return min_(montant_qf, bareme_age.calc(age))


class strasbourg_piscine_entree_unitaire(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH


class strasbourg_piscine_10_entrees_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        age = individu("age", period.first_month)

        reduit = individu("strasbourg_sports_reduit", period)

        bareme_age = parameters(
            period
        ).communes.strasbourg.piscine._10_entrees.bareme_age
        bareme_qf = parameters(period).communes.strasbourg.piscine._10_entrees.bareme_qf
        bareme_qf_reduit = parameters(period).communes.strasbourg.piscine._10_entrees.bareme_qf_reduit

        montant_reduit = bareme_qf_reduit.calc(qf)
        montant = bareme_qf.calc(qf)
        montant_qf = np.where(reduit, min_(montant_reduit, montant+individu('sslr', period)), montant)
        return min_(montant_qf, bareme_age.calc(age))


class strasbourg_piscine_10_entrees(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH


class strasbourg_piscine_5_entrees_ce_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme_qf = parameters(period).communes.strasbourg.piscine.ce.entrees
        return bareme_qf.calc(qf)


class strasbourg_piscine_cycle_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme_qf = parameters(period).communes.strasbourg.piscine.cycle.bareme
        return bareme_qf.calc(qf)


class strasbourg_piscine_cycle2_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        return 2 * individu("strasbourg_piscine_cycle_prix", period)

class strasbourg_piscine_stage_ete_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme_qf = parameters(period).communes.strasbourg.piscine.stage_ete.bareme
        return bareme_qf.calc(qf)


class strasbourg_piscine_stage_vacances_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme_qf = parameters(period).communes.strasbourg.piscine.stage_vacances.bareme
        return bareme_qf.calc(qf)


class strasbourg_piscine_stage_5_seances_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme_qf = parameters(
            period
        ).communes.strasbourg.piscine.stage_5_seances.bareme
        return bareme_qf.calc(qf)


class strasbourg_piscine_activite_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme_qf = parameters(
            period
        ).communes.strasbourg.piscine.activite.unitaire
        return bareme_qf.calc(qf)


class strasbourg_piscine_activite_10_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme_qf = parameters(
            period
        ).communes.strasbourg.piscine.activite._10
        return bareme_qf.calc(qf)


class strasbourg_piscine_aquabike_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme_qf = parameters(
            period
        ).communes.strasbourg.piscine.aquabike.unitaire
        return bareme_qf.calc(qf)


class strasbourg_piscine_aquabike_cycle_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme_qf = parameters(
            period
        ).communes.strasbourg.piscine.aquabike.cycle
        return bareme_qf.calc(qf)
