from openfisca_france.model.base import Variable, Individu, Menage, MONTH, not_, TypesActivite
from numpy.core.defchararray import startswith


class grand_est_fluo_67_pertinence_geographique(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Pertinence d'afficher les dispositifs pour le réseau Fluo 67"

    def formula(menage, period):
        depcom = menage('depcom', period)
        return startswith(depcom, b'67')


class grand_est_fluo_67_tarification_solidaire(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Tarification solidaire des transports du réseau Fluo 67"
    reference = [
        "https://www.ctbr67.fr/tarifs/tarifs-reduits-gratuite/"
        ]

    def formula(individu, period):
        geo = individu.menage('grand_est_fluo_67_pertinence_geographique', period)
        aah = individu('aah', period)
        aspa = individu.famille('aspa', period)
        gratuit = individu('grand_est_fluo_67_eligible_gratuite', period)
        return 26 * geo * ((aah > 0) + (aspa > 0))


class grand_est_fluo_67_eligible_gratuite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité à la gratuité des transports du réseau Fluo 67"
    reference = [
        "https://www.ctbr67.fr/tarifs/tarifs-reduits-gratuite/"
        ]

    def formula(individu, period):
        geo = individu.menage('grand_est_fluo_67_pertinence_geographique', period)
        chomeur = individu('activite', period) == TypesActivite.chomeur
        rsa = individu.famille('rsa', period)
        return geo * (chomeur + rsa > 0)
