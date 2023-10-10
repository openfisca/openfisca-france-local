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


class strasbourg_centre_choregraphique_eveil_2trimestre_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)

        baremes = parameters(period).communes.strasbourg.centre_choregraphique.eveil_trimestre
        return 2 * np.select(
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


class strasbourg_centre_choregraphique_adulte_extra_cours_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.adulte
        return baremes.extra_cours.calc(qf)


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


class strasbourg_centre_choregraphique_enfant_1_cours_2trimestre_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)

        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.enfant._1_cours_trimestre
        return 2 * np.select(
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



class strasbourg_centre_choregraphique_enfant_2_cours_trimestre_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)

        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.enfant._2_cours_trimestre
        return np.select(
            [tarif == CCSTarif.RA, tarif == CCSTarif.RB],
            [baremes.RA.calc(qf), baremes.RB.calc(qf)],
            default=baremes.TP.calc(qf),
        )


class strasbourg_centre_choregraphique_adulte_2_cours_2trimestre_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)

        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.adulte._2_cours_trimestre
        return 2 * np.select(
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


class strasbourg_centre_choregraphique_enfant_4_cours_trimestre_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)

        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.enfant._4_cours_trimestre
        return np.select(
            [tarif == CCSTarif.RA, tarif == CCSTarif.RB],
            [baremes.RA.calc(qf), baremes.RB.calc(qf)],
            default=baremes.TP.calc(qf),
        )


class strasbourg_centre_choregraphique_enfant_extra_cours_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.enfant.extra_cours
        return baremes.calc(qf)


class strasbourg_centre_choregraphique_enfant_stage_1semaine_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)
        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.enfant.stage_journee
        return 5 * np.select(
            [tarif == CCSTarif.RC],
            [baremes.RC.calc(qf)],
            default=baremes.TP.calc(qf),
        )


class strasbourg_centre_choregraphique_adulte_stage_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        tarif = individu.famille("strasbourg_centre_choregraphique_tarif", period)

        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.adulte.stage
        return np.select(
            [tarif == CCSTarif.RC],
            [baremes.RC.calc(qf)],
            default=baremes.TP.calc(qf),
        )


class strasbourg_centre_choregraphique_adulte_stage_130_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        stage = individu("strasbourg_centre_choregraphique_adulte_stage_prix", period)

        return 1.5* stage

class strasbourg_centre_choregraphique_adulte_stage_2_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        stage = individu("strasbourg_centre_choregraphique_adulte_stage_prix", period)

        return 2* stage

class strasbourg_centre_choregraphique_adulte_stage_3_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        stage = individu("strasbourg_centre_choregraphique_adulte_stage_prix", period)

        return 3 * stage

class strasbourg_centre_choregraphique_adulte_stage_4_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        stage = individu("strasbourg_centre_choregraphique_adulte_stage_prix", period)

        return 4* stage

class strasbourg_centre_choregraphique_adulte_stage_430_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        stage = individu("strasbourg_centre_choregraphique_adulte_stage_prix", period)

        return 4.5* stage

class strasbourg_centre_choregraphique_adulte_stage_6_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        stage = individu("strasbourg_centre_choregraphique_adulte_stage_prix", period)

        return 6* stage

class strasbourg_centre_choregraphique_adulte_stage_8_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        stage = individu("strasbourg_centre_choregraphique_adulte_stage_prix", period)

        return 8* stage

class strasbourg_centre_choregraphique_adulte_stage_1semaine_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        qf = individu.famille("strasbourg_metropole_quotient_familial", period)
        baremes = parameters(
            period
        ).communes.strasbourg.centre_choregraphique.adulte.stage_semaine
        return baremes.calc(qf)


class strasbourg_centre_choregraphique_adulte_1_cours_2trimestre_prix(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        trimestre = individu("strasbourg_centre_choregraphique_adulte_1_cours_trimestre_prix", period)

        return 2 * trimestre
