from openfisca_france.model.base import *

class strasbourg_periscolaire_maternelle_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme = parameters(period).communes.strasbourg.periscolaire_maternelle.bareme_journee
        return bareme.calc(qf)

class strasbourg_periscolaire_maternelle_nombre(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH


class strasbourg_periscolaire_maternelle_cout(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        prix = individu("strasbourg_periscolaire_maternelle_prix", period)
        nb = individu("strasbourg_periscolaire_maternelle_nombre", period)
        return nb*prix


class strasbourg_periscolaire_maternelle_matin_ou_soir_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme = parameters(period).communes.strasbourg.periscolaire_maternelle.bareme_matin_ou_soir
        return bareme.calc(qf)


class strasbourg_periscolaire_maternelle_matin_ou_soir_nombre(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH


class strasbourg_periscolaire_maternelle_matin_ou_soir_cout(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        prix = individu("strasbourg_periscolaire_maternelle_matin_ou_soir_prix", period)
        nb = individu("strasbourg_periscolaire_maternelle_matin_ou_soir_nombre", period)
        return nb*prix
