from openfisca_france.model.base import *
import numpy as np

class strasbourg_piscine_abonnement_annuel(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH

class strasbourg_prix_piscine_abonnement_annuel(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        abo = individu("strasbourg_piscine_abonnement_annuel", period)

        taux_incapacite = individu('taux_incapacite', period)
        qf_ajus = np.where(taux_incapacite, 400, qf)

        bareme = parameters(period).communes.strasbourg.piscine.abonnement_annuel
        return abo * bareme.calc(qf_ajus)


class strasbourg_piscine_abonnement_ce(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH


class strasbourg_prix_piscine_abonnement_ce(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        abo = individu("strasbourg_piscine_abonnement_ce", period)
        return abo * 140


class strasbourg_piscine_abonnement_ete(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH


class strasbourg_prix_piscine_abonnement_ete(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        abo = individu("strasbourg_piscine_abonnement_ete", period)
        bareme = parameters(period).communes.strasbourg.piscine.abonnement_ete
        return abo * bareme.calc(qf)


class strasbourg_piscine_prix_entree_unitaire(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        age = individu("age", period.first_month)

        taux_incapacite = individu('taux_incapacite', period)
        qf_ajus = np.where(taux_incapacite, 400, qf)

        bareme_age = parameters(period).communes.strasbourg.piscine.entree_unitaire.bareme_age
        bareme_qf = parameters(period).communes.strasbourg.piscine.entree_unitaire.bareme_qf
        return min_(bareme_qf.calc(qf_ajus), bareme_age.calc(age))

class strasbourg_piscine_entree_unitaire(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH

class strasbourg_piscine_prix_10_entrees(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        age = individu("age", period.first_month)
        taux_incapacite = individu('taux_incapacite', period)

        qf_ajus = np.where(taux_incapacite, 400, qf)

        bareme_age = parameters(period).communes.strasbourg.piscine._10_entrees.bareme_age
        bareme_qf = parameters(period).communes.strasbourg.piscine._10_entrees.bareme_qf
        return min_(bareme_qf.calc(qf_ajus), bareme_age.calc(age))


class strasbourg_piscine_10_entrees(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH


class strasbourg_prix_piscine_5_entrees_ce(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        return 15


class strasbourg_prix_piscine_cycle(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme_qf = parameters(period).communes.strasbourg.piscine.cycle.bareme
        return bareme_qf.calc(qf)


class strasbourg_prix_piscine_stage_ete(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme_qf = parameters(period).communes.strasbourg.piscine.stage_ete.bareme
        return bareme_qf.calc(qf)


class strasbourg_prix_piscine_stage_vacances(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme_qf = parameters(period).communes.strasbourg.piscine.stage_vacances.bareme
        return bareme_qf.calc(qf)


class strasbourg_prix_piscine_stage_5_seances(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme_qf = parameters(period).communes.strasbourg.piscine.stage_5_seances.bareme
        return bareme_qf.calc(qf)
