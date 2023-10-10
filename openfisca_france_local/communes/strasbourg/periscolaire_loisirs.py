from openfisca_france.model.base import *

class strasbourg_periscolaire_loisirs_journee_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme = parameters(period).communes.strasbourg.periscolaire_loisirs.journee.bareme
        return bareme.calc(qf)


class strasbourg_periscolaire_loisirs_journee_nombre(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH


class strasbourg_periscolaire_loisirs_journee_cout(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        prix = individu("strasbourg_periscolaire_loisirs_journee_prix", period)
        nb = individu("strasbourg_periscolaire_loisirs_journee_nombre", period)
        return nb*prix


class strasbourg_periscolaire_loisirs_demi_journee_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme = parameters(period).communes.strasbourg.periscolaire_loisirs.demi_journee.bareme
        return bareme.calc(qf)


class strasbourg_periscolaire_loisirs_demi_journee_nombre(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH


class strasbourg_periscolaire_loisirs_demi_journee_cout(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        prix = individu("strasbourg_periscolaire_loisirs_journee_prix", period)
        nb = individu("strasbourg_periscolaire_loisirs_journee_nombre", period)
        return nb*prix


class strasbourg_periscolaire_loisirs_repas_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme = parameters(period).metropoles.strasbourg.tarifs_cantine
        return bareme.calc(qf)


class strasbourg_periscolaire_loisirs_repas_nombre(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH


class strasbourg_periscolaire_loisirs_repas_cout(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        prix = individu("strasbourg_periscolaire_loisirs_repas_prix", period)
        nb = individu("strasbourg_periscolaire_loisirs_repas_nombre", period)
        return nb*prix


class strasbourg_periscolaire_loisirs_panier_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        bareme = parameters(period).metropoles.strasbourg.tarifs_repas_panier
        return bareme.calc(qf)


class strasbourg_periscolaire_loisirs_panier_nombre(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH


class strasbourg_periscolaire_loisirs_panier_cout(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        prix = individu("strasbourg_periscolaire_loisirs_panier_prix", period)
        nb = individu("strasbourg_periscolaire_loisirs_panier_nombre", period)
        return nb*prix
