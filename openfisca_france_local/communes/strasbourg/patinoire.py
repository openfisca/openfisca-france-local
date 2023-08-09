from openfisca_france.model.base import *
import numpy as np

class strasbourg_prix_patinoire_entree_unitaire(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        age = individu("age", period.first_month)

        taux_incapacite = individu('taux_incapacite', period)
        qf_ajus = np.where(taux_incapacite, 400, qf)

        bareme_age = parameters(period).communes.strasbourg.patinoire.entree_unitaire.bareme_age
        bareme_qf = parameters(period).communes.strasbourg.patinoire.entree_unitaire.bareme_qf
        return min_(bareme_qf.calc(qf_ajus), bareme_age.calc(age))

class strasbourg_patinoire_entree_unitaire(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH


class strasbourg_prix_patinoire_10_entrees(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        age = individu("age", period.first_month)

        taux_incapacite = individu('taux_incapacite', period)
        qf_ajus = np.where(taux_incapacite, 400, qf)

        bareme_age = parameters(period).communes.strasbourg.patinoire._10_entrees.bareme_age
        bareme_qf = parameters(period).communes.strasbourg.patinoire._10_entrees.bareme_qf
        return min_(bareme_qf.calc(qf_ajus), bareme_age.calc(age))


class strasbourg_prix_patinoire_5_entrees_ce(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        return 22
