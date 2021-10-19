from openfisca_france.model.base import Variable, Menage, MONTH
from numpy.core.defchararray import startswith

DEPARTEMENTS_OCCITANIE = [
    b"09", b"11", b"12", b"30", b"31", b"32", b"34", b"46", b"48", b"65", b"66", b"81", b"82"
]

class occitanie_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la région Occitanie"

    def formula(menage, period):
        depcom = menage('depcom', period)
        return sum([startswith(depcom, code_departement) for code_departement in DEPARTEMENTS_OCCITANIE]) > 0

