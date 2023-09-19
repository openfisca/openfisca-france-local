from openfisca_france.model.base import Variable, Individu, Famille, MONTH, select, max_


class strasbourg_metropole_quotient_familial(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Quotient familial de l'Eurométropole de Strasbourg"

    def formula(famille, period):
        return famille('qf_caf', period)


class qf_caf(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

    def formula(famille, period):
        return famille.demandeur.foyer_fiscal('rfr', period.n_2) / 12 / famille.demandeur.foyer_fiscal('nbptr', period.n_2)


class qf_fiscal(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

    def formula(famille, period):
        return famille.demandeur.foyer_fiscal('rfr', period.n_2) / 12 / famille.demandeur.foyer_fiscal('nbptr', period.n_2)


class sample_id(Variable):
    value_type = int
    entity = Famille
    definition_period = MONTH


class TYPOLOGIE(Variable):
    value_type = str
    entity = Famille
    definition_period = MONTH
