from openfisca_france.model.base import *

class strasbourg_piscine_quotient_familial(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR

class strasbourg_piscine_abonnement_annuel(Variable):
    value_type = bool
    entity = Individu
    definition_period = YEAR

class strasbourg_prix_piscine_abonnement_annuel(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
 
    def formula(individu, period, parameters):
        qf = individu("strasbourg_piscine_quotient_familial", period)
        abo = individu("strasbourg_piscine_abonnement_annuel", period)
        bareme = parameters(period).communes.strasbourg.piscine.abonnement_annuel
        return abo * bareme.calc(qf)

class strasbourg_piscine_abonnement_ete(Variable):
    value_type = bool
    entity = Individu
    definition_period = YEAR


class strasbourg_prix_piscine_abonnement_ete(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR

    def formula(individu, period, parameters):
        qf = individu("strasbourg_piscine_quotient_familial", period)
        abo = individu("strasbourg_piscine_abonnement_ete", period)
        bareme = parameters(period).communes.strasbourg.piscine.abonnement_ete
        return abo * bareme.calc(qf)


class strasbourg_piscine_prix_entree_unitaire(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR

    def formula(individu, period, parameters):
        qf = individu("strasbourg_piscine_quotient_familial", period)
        age = individu("age", period.first_month)
        bareme_age = parameters(period).communes.strasbourg.piscine.entree_unitaire.bareme_age
        bareme_qf = parameters(period).communes.strasbourg.piscine.entree_unitaire.bareme_qf
        return min_(bareme_qf.calc(qf), bareme_age.calc(age))

class strasbourg_piscine_entree_unitaire(Variable):
    value_type = int
    entity = Individu
    definition_period = YEAR

class strasbourg_piscine_cout_entree_unitaire(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR

    def formula(individu, period, parameters):
        prix = individu("strasbourg_piscine_prix_entree_unitaire", period)
        nb = individu("strasbourg_piscine_entree_unitaire", period)
        return nb * prix
