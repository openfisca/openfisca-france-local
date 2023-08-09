from openfisca_france.model.base import *

class strasbourg_prix_periscolaire_loisirs_journee(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
 
    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme = parameters(period).communes.strasbourg.periscolaire_loisirs.journee.bareme
        return bareme.calc(qf)


class strasbourg_prix_periscolaire_loisirs_demi_journee(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
 
    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme = parameters(period).communes.strasbourg.periscolaire_loisirs.demi_journee.bareme
        return bareme.calc(qf)


class strasbourg_prix_periscolaire_loisirs_repas(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
 
    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme = parameters(period).metropoles.strasbourg.tarifs_cantine
        return bareme.calc(qf)


class strasbourg_prix_periscolaire_loisirs_panier(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
 
    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme = parameters(period).metropoles.strasbourg.tarifs_repas_panier
        return bareme.calc(qf)
