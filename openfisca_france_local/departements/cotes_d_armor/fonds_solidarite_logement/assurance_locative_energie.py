# -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france_local.departements.cotes_d_armor.fonds_solidarite_logement.base_ressource import bareme_de_base


class cotes_d_armor_fonds_solidarite_logement_assurance_locative_energie_plafond(Variable):
    value_type = float
    entity = Menage
    definition_period = MONTH

    def formula(menage, period, parameters):
        bareme = parameters(period).departements.cotes_d_armor.fonds_solidarite_logement.assurance_locative_energie.bareme
        return bareme_de_base(bareme, menage.nb_persons())


class cotes_d_armor_fonds_solidarite_logement_assurance_locative_energie_eligibilite_financiere(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH

    def formula(menage, period, parameters):
        br = menage('cotes_d_armor_fonds_solidarite_logement_base_ressource_moyennee', period)
        plafond = menage('cotes_d_armor_fonds_solidarite_logement_assurance_locative_energie_plafond', period)
        return br < plafond


class cotes_d_armor_fonds_solidarite_logement_assurance_locative_energie_eligibilite(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH

    def formula(menage, period, parameters):
        resid = menage('cotes_d_armor_eligibilite_residence', period)
        financier = menage('cotes_d_armor_fonds_solidarite_logement_assurance_locative_energie_eligibilite_financiere', period)
        return resid * financier


class cotes_d_armor_fonds_solidarite_logement_assurance_locative_eligibilite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        return individu.menage('cotes_d_armor_fonds_solidarite_logement_assurance_locative_energie_eligibilite', period)


class cotes_d_armor_fonds_solidarite_logement_energie_eligibilite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        return individu.menage('cotes_d_armor_fonds_solidarite_logement_assurance_locative_energie_eligibilite', period)
