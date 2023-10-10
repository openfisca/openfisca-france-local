from openfisca_france.model.base import *
import numpy as np

class strasbourg_patinoire_entree_unitaire_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        age = individu("age", period.first_month)
        reduit = individu("strasbourg_sports_reduit", period)

        bareme_age = parameters(period).communes.strasbourg.patinoire.entree_unitaire.bareme_age
        bareme_qf = parameters(period).communes.strasbourg.patinoire.entree_unitaire.bareme_qf
        bareme_qf_reduit = parameters(period).communes.strasbourg.patinoire.entree_unitaire.bareme_qf_reduit

        montant_reduit = bareme_qf_reduit.calc(qf)
        montant = bareme_qf.calc(qf)
        montant_qf = np.where(reduit, min_(montant_reduit, montant+individu('sslr', period)), montant)
        return min_(montant_qf, bareme_age.calc(age))


class strasbourg_patinoire_entree_unitaire(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH


class strasbourg_patinoire_10_entrees_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        age = individu("age", period.first_month)
        reduit = individu("strasbourg_sports_reduit", period)

        bareme_age = parameters(period).communes.strasbourg.patinoire._10_entrees.bareme_age
        bareme_qf = parameters(period).communes.strasbourg.patinoire._10_entrees.bareme_qf
        bareme_qf_reduit = parameters(period).communes.strasbourg.patinoire._10_entrees.bareme_qf_reduit

        montant_reduit = bareme_qf_reduit.calc(qf)
        montant = bareme_qf.calc(qf)
        montant_qf = np.where(reduit, min_(montant_reduit, montant+individu('sslr', period)), montant)
        return min_(montant_qf, bareme_age.calc(age))


class strasbourg_patinoire_5_entrees_ce_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme = parameters(period).communes.strasbourg.patinoire.ce.entrees
        return bareme.calc(qf)


class strasbourg_patinoire_ecole_de_glace_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme = parameters(period).communes.strasbourg.patinoire.ecole_de_glace
        return bareme.calc(qf)
