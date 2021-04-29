from openfisca_france.model.base import Variable, Individu, Famille, MONTH, select, max_


class strasbourg_metropole_quotient_familial(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Quotient familial pour la tarification solidaire de la cantine de l'Eurométropole de Strasbourg"

    def formula(famille, period):
        return famille.demandeur.foyer_fiscal('rfr', period.n_2) / 12 / famille.demandeur.foyer_fiscal('nbptr', period.n_2)


class strasbourg_metropole_tarification_cantine(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Quotient familial pour la tarification solidaire de la cantine de l'Eurométropole de Strasbourg"

    def formula(famille, period, parameters):
        qf = famille('strasbourg_metropole_quotient_familial', period)
        tarif = parameters(period).metropoles.strasbourg.tarifs_cantine
        return tarif.calc(max_(0, qf), right=True)


class strasbourg_metropole_nombre_repas_cantine(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH


class strasbourg_metropole_cout_cantine(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        cout_individu = famille.members('strasbourg_metropole_cout_cantine_individu', period)
        return famille.sum(cout_individu)


# class strasbourg_metropole_cout_cantine2(Variable):
#     value_type = float
#     entity = Famille
#     definition_period = MONTH

#     def formula(famille, period, parameters):
#         tarif = famille('strasbourg_metropole_tarification_cantine')
#         cout_individu = famille.members('strasbourg_metropole_cout_cantine_individu', period)
#         return famille.sum(cout_individu * famille.spread(tarif))


class strasbourg_metropole_cout_cantine_individu(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        tarif = individu.famille('strasbourg_metropole_tarification_cantine', period)
        repas = individu('strasbourg_metropole_nombre_repas_cantine', period)
        return tarif * repas

#variables repas végétarien 

class strasbourg_metropole_tarification_cantine_vegetarien(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Quotient familial pour la tarification solidaire de la cantine pour un repas végétarien de l'Eurométropole de Strasbourg"

    def formula(famille, period, parameters):
        qf = famille('strasbourg_metropole_quotient_familial', period)
        tarif = parameters(period).metropoles.strasbourg.tarifs_repas_vege
        return tarif.calc(max_(0, qf), right=True)


class strasbourg_metropole_cout_cantine_repas_vegetarien(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        cout_individu = famille.members('strasbourg_metropole_cout_cantine_individu_repas_vegetarien', period)
        return famille.sum(cout_individu)


class strasbourg_metropole_cout_cantine_individu_repas_vegetarien(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        tarif = individu.famille('strasbourg_metropole_tarification_cantine_vegetarien', period)
        repas = individu('strasbourg_metropole_nombre_repas_cantine_vegetarien', period)
        return tarif * repas

class strasbourg_metropole_nombre_repas_cantine_vegetarien(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    