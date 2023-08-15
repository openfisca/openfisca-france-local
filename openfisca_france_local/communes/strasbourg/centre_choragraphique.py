from openfisca_france.model.base import *
import numpy as np

from openfisca_france_local.communes.strasbourg.statuts import CCSTarif

class strasbourg_centre_choregraphique_eveil_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)

        baremes = parameters(period).communes.strasbourg.centre_choregraphique.eveil
        return np.select(
            [tarif == CCSTarif.RA, tarif == CCSTarif.RB],
            [baremes.RA.calc(qf), baremes.RB.calc(qf)],
            default=baremes.TP.calc(qf),
        )


class strasbourg_centre_choregraphique_adulte_1_cours_trimestre_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)

        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.adulte._1_cours_trimestre
        return np.select(
            [tarif == CCSTarif.RA, tarif == CCSTarif.RB],
            [baremes.RA.calc(qf), baremes.RB.calc(qf)],
            default=baremes.TP.calc(qf),
        )


class strasbourg_centre_choregraphique_adulte_1_cours_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)
        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.adulte._1_cours
        return np.select(
            [tarif == CCSTarif.RA, tarif == CCSTarif.RB],
            [baremes.RA.calc(qf), baremes.RB.calc(qf)],
            default=baremes.TP.calc(qf),
        )


class strasbourg_centre_choregraphique_adulte_2_cours_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)

        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.adulte._2_cours
        return np.select(
            [tarif == CCSTarif.RA, tarif == CCSTarif.RB],
            [baremes.RA.calc(qf), baremes.RB.calc(qf)],
            default=baremes.TP.calc(qf),
        )


class strasbourg_centre_choregraphique_adulte_3_cours_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)

        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.adulte._3_cours
        return np.select(
            [tarif == CCSTarif.RA, tarif == CCSTarif.RB],
            [baremes.RA.calc(qf), baremes.RB.calc(qf)],
            default=baremes.TP.calc(qf),
        )


class strasbourg_centre_choregraphique_adulte_4_cours_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)

        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.adulte._4_cours
        return np.select(
            [tarif == CCSTarif.RA, tarif == CCSTarif.RB],
            [baremes.RA.calc(qf), baremes.RB.calc(qf)],
            default=baremes.TP.calc(qf),
        )


class strasbourg_centre_choregraphique_enfant_1_cours_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)

        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.enfant._1_cours
        return np.select(
            [tarif == CCSTarif.RA, tarif == CCSTarif.RB],
            [baremes.RA.calc(qf), baremes.RB.calc(qf)],
            default=baremes.TP.calc(qf),
        )


class strasbourg_centre_choregraphique_enfant_2_cours_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)

        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.enfant._2_cours
        return np.select(
            [tarif == CCSTarif.RA, tarif == CCSTarif.RB],
            [baremes.RA.calc(qf), baremes.RB.calc(qf)],
            default=baremes.TP.calc(qf),
        )


class strasbourg_centre_choregraphique_enfant_3_cours_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)

        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.enfant._3_cours
        return np.select(
            [tarif == CCSTarif.RA, tarif == CCSTarif.RB],
            [baremes.RA.calc(qf), baremes.RB.calc(qf)],
            default=baremes.TP.calc(qf),
        )


class strasbourg_centre_choregraphique_enfant_4_cours_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)

        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.enfant._4_cours
        return np.select(
            [tarif == CCSTarif.RA, tarif == CCSTarif.RB],
            [baremes.RA.calc(qf), baremes.RB.calc(qf)],
            default=baremes.TP.calc(qf),
        )
