from openfisca_france.model.base import Variable, Menage, MONTH

from numpy.core.defchararray import startswith


class auvergne_rhone_alpes_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la région Auvergne-Rhône-Alpes."

    def formula(menage, period, parameters):
        depcom = menage('depcom', period)
        return sum([startswith(depcom, str.encode(code)) for code in parameters(period).regions.auvergne_rhone_alpes.departements]) > 0
