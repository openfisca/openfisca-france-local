from openfisca_france.model.base import Variable, Individu, MONTH, select


class strasbourg_metropole_quotient_familial(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Quotient familial pour la tarification solidaire de la cantine de l'Eurométropole de Strasbourg"


class strasbourg_metropole_tarification_cantine(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Quotient familial pour la tarification solidaire de la cantine de l'Eurométropole de Strasbourg"
    
    def formula(individu, period, parameters):
        qf = individu('strasbourg_metropole_quotient_familial', period)
        tarif = parameters(period).metropoles.strasbourg.tarifs_cantine
        return tarif.calc(qf)
        # return (qf <= 410) + (qf <= 510) + (qf <= 620) + (qf <= 720) + (qf <= 820) + (qf <= 920) + (qf <= 1030) + (qf <= 1540) + (qf <= 2050)
        return select(
            [qf <= 410],
            [1.50],
            default=2.15)
          
