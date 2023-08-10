from openfisca_france.model.base import *

class strasbourg_periscolaire_maternelle_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
 
    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme = parameters(period).communes.strasbourg.periscolaire_maternelle.bareme
        return bareme.calc(qf)
