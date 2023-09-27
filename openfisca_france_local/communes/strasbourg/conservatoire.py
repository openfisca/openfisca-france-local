from openfisca_france.model.base import *
import numpy as np

class strasbourg_conservatoire_enfant_dans_la_fratrie(Variable):
    value_type = int
    entity = Famille
    definition_period = MONTH


class strasbourg_conservatoire_base_ressources(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

    def formula(famille, period):
        return famille.demandeur.foyer_fiscal("rni", period.n_2)


class strasbourg_conservatoire_autre_dominante(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        qf = famille('strasbourg_conservatoire_base_ressources', period)
        P = parameters(period).communes.strasbourg.conservatoire.autre_dominante
        return P.calc(qf)


class strasbourg_conservatoire_parcours_personnalise(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        qf = famille('strasbourg_conservatoire_base_ressources', period)
        P = parameters(period).communes.strasbourg.conservatoire.parcours_personnalise
        return P.calc(qf)


class strasbourg_conservatoire_traditionnel_enf12(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        qf = famille('strasbourg_conservatoire_base_ressources', period)
        P = parameters(period).communes.strasbourg.conservatoire.traditionnel

        agent_ems = famille("agent_ems", period)
        habitant_ems = famille("habitant_ems", period)
        return np.select([agent_ems, habitant_ems], [
            P.agent_ems.enfant_12.calc(qf),
            P.habitant_ems.enfant_12.calc(qf),
            ], default = P.hors_ems.enfant_12.calc(qf))


class strasbourg_conservatoire_traditionnel_enf3(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        qf = famille('strasbourg_conservatoire_base_ressources', period)
        P = parameters(period).communes.strasbourg.conservatoire.traditionnel
        return P.enfant_3.calc(qf)


class strasbourg_conservatoire_horaires_amenages_enf1(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        qf = famille('strasbourg_conservatoire_base_ressources', period)
        P = parameters(period).communes.strasbourg.conservatoire.horaires_amenages

        habitant_ems = famille("habitant_ems", period)
        return np.where(habitant_ems,
            P.habitant_ems.enfant_1.calc(qf),
            P.hors_ems.enfant_1.calc(qf))



class strasbourg_conservatoire_horaires_amenages_enf2(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        qf = famille('strasbourg_conservatoire_base_ressources', period)
        P = parameters(period).communes.strasbourg.conservatoire.horaires_amenages

        habitant_ems = famille("habitant_ems", period)
        return np.where(habitant_ems,
            P.habitant_ems.enfant_2.calc(qf),
            P.hors_ems.enfant_2.calc(qf))



class strasbourg_conservatoire_horaires_amenages_enf3(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        qf = famille('strasbourg_conservatoire_base_ressources', period)
        P = parameters(period).communes.strasbourg.conservatoire.horaires_amenages

        habitant_ems = famille("habitant_ems", period)
        return np.where(habitant_ems,
            P.habitant_ems.enfant_3.calc(qf),
            P.hors_ems.enfant_3.calc(qf))



class strasbourg_conservatoire_horaires_amenages_enf4(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        qf = famille('strasbourg_conservatoire_base_ressources', period)
        P = parameters(period).communes.strasbourg.conservatoire.horaires_amenages

        habitant_ems = famille("habitant_ems", period)
        return np.where(habitant_ems,
            P.habitant_ems.enfant_4.calc(qf),
            P.hors_ems.enfant_4.calc(qf))


class strasbourg_conservatoire_nombre_cycles(Variable):
    value_type = int
    entity = Famille
    definition_period = MONTH


class strasbourg_conservatoire_cycles(Variable):
    value_type = int
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        nb = famille('strasbourg_conservatoire_nombre_cycles', period)
        qf = famille('strasbourg_conservatoire_base_ressources', period)
        P = parameters(period).communes.strasbourg.conservatoire.cycle

        return nb*P.calc(qf)


class strasbourg_conservatoire_qf_bourse(Variable):
    value_type = int
    entity = Famille
    definition_period = MONTH


class strasbourg_conservatoire_bourse(Variable):
    value_type = int
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        qf = famille('strasbourg_conservatoire_qf_bourse', period)
        P = parameters(period).communes.strasbourg.conservatoire.bourse

        return -P.calc(qf)
