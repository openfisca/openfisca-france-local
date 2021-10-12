from openfisca_france.model.base import Variable, Menage, MONTH

from numpy.core.defchararray import startswith

DEPARTEMENT_AUVERGNE_RHONE_ALPES = [b'01', b'03', b'07', b'15', b'26', b'42', b'43', b'63', b'69', b'73', b'74']

class auvergne_rhone_alpes_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la région Auvergne-Rhône-Alpes."

    def formula(menage, period):
        depcom = menage('depcom', period)
        return sum([startswith(depcom, code) for code in DEPARTEMENT_AUVERGNE_RHONE_ALPES]) > 0
