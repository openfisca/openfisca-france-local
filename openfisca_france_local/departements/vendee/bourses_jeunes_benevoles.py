from openfisca_france.model.base import *
from numpy.core.defchararray import startswith


class vendee_bourses_jeunes_benevoles_montant_max(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Montant maximum des bourses aux jeunes bénévoles vendéens"
    reference = [
        "https://benevolat.vendee.fr/content/download/270/1700/file/reglement%20BJBV_2020.pdf"
    ]

    def formula(individu, period):
        age = individu('age', period)
        depcom = individu.menage('depcom', period)

        eligibilite_geographique = startswith(depcom, b'85')

        eligible = eligibilite_geographique * (age >= 16) * (age <= 25)
        return 800 * eligible
