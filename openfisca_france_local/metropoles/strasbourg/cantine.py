from openfisca_france.model.base import Variable, Individu, MONTH, select, max_


class strasbourg_metropole_quotient_familial(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Quotient familial pour la tarification solidaire de la cantine de l'Eurométropole de Strasbourg"

    def formula(individu, period):
        return individu.foyer_fiscal('rfr', period.n_2) / 12 / individu.foyer_fiscal('nbptr', period.n_2)


class strasbourg_metropole_tarification_cantine(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Quotient familial pour la tarification solidaire de la cantine de l'Eurométropole de Strasbourg"
    
    def formula(individu, period, parameters):
        qf = individu('strasbourg_metropole_quotient_familial', period)
        tarif = parameters(period).metropoles.strasbourg.tarifs_cantine
        return tarif.calc(max_(0, qf), right=True)
