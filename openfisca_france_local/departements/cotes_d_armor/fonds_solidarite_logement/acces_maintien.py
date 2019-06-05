# -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france_local.departements.cotes_d_armor.fonds_solidarite_logement.base_ressource import bareme_de_base


class cotes_d_armor_fonds_solidarite_logement_acces_maintien_taux_effort(Variable):
    value_type = float
    entity = Menage
    definition_period = MONTH
    reference = [
        'Chapitre 4 page 8 du Réglement intérieur',
    ]

    def formula(menage, period, parameters):
        loyer = menage('loyer', period)
        al = menage.personne_de_reference.famille('aide_logement', period)
        br = menage('cotes_d_armor_fonds_solidarite_logement_base_ressource_moyennee', period)

        return (loyer - al) / br


class cotes_d_armor_fonds_solidarite_logement_acces_maintien_loyer_adapte(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    reference = [
        'Chapitre 4 page 8 du Réglement intérieur',
    ]

    def formula(menage, period, parameters):
        taux_effort = menage('cotes_d_armor_fonds_solidarite_logement_acces_maintien_taux_effort', period)
        taux_effort_maximum = parameters(period).departements.cotes_d_armor.fonds_solidarite_logement.acces_maintien.taux_effort_maximum

        return taux_effort <= taux_effort_maximum


class cotes_d_armor_fonds_solidarite_logement_acces_maintien_plafond(Variable):
    value_type = float
    entity = Menage
    definition_period = MONTH
    reference = [
        'Annexe 2 page 21 du Réglement intérieur',
    ]

    def formula(menage, period, parameters):
        bareme = parameters(period).departements.cotes_d_armor.fonds_solidarite_logement.acces_maintien.bareme
        return bareme_de_base(bareme, menage.nb_persons())


class cotes_d_armor_fonds_solidarite_logement_acces_maintien_eligibilite_financiere(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    reference = [
        'Annexe 2 page 21 du Réglement intérieur',
    ]

    def formula(menage, period, parameters):
        br = menage('cotes_d_armor_fonds_solidarite_logement_base_ressource_moyennee', period)
        plafond = menage('cotes_d_armor_fonds_solidarite_logement_acces_maintien_plafond', period)
        return br < plafond


class cotes_d_armor_fonds_solidarite_logement_acces_maintien_eligibilite(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH

    def formula(menage, period, parameters):
        resid = menage('cotes_d_armor_eligibilite_residence', period)
        loyer_adapte = menage('cotes_d_armor_fonds_solidarite_logement_acces_maintien_loyer_adapte', period)
        financier = menage('cotes_d_armor_fonds_solidarite_logement_acces_maintien_eligibilite_financiere', period)
        return resid * loyer_adapte * financier


class cotes_d_armor_fonds_solidarite_logement_acces_eligibilite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        return individu.menage('cotes_d_armor_fonds_solidarite_logement_acces_maintien_eligibilite', period)


class cotes_d_armor_fonds_solidarite_logement_maintien_eligibilite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        return individu.menage('cotes_d_armor_fonds_solidarite_logement_acces_maintien_eligibilite', period)
