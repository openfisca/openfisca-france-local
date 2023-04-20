from numpy.core.defchararray import startswith

from openfisca_france.model.base import Individu, MONTH, Variable
from openfisca_france.model.caracteristiques_socio_demographiques.demographie import RegimeSecuriteSociale

code_departements = [b'09', b'31', b'32', b'65']


class msa_midi_pyrenees_sud_aide_permis(Variable):
    value_type = float
    entity = Individu
    label = "Éligibilité financière à l'aide à l’obtention du permis de conduire de la MSA Midi-Pyrénées Sud"
    reference = "https://mps.msa.fr/lfy/famille/aide-permis-de-conduire"
    definition_period = MONTH

    def formula(individu, period, parameters):
        params = parameters(period).regions.occitanie.msa_midi_pyrenees_sud.aide_permis

        montant = params.montant

        depcom = individu.menage('depcom', period)
        eligibilite_geographique = sum([startswith(depcom, code_departement) for code_departement in code_departements])

        allocataire_msa = individu('regime_securite_sociale', period) == RegimeSecuriteSociale.regime_agricole

        age = individu('age', period)
        eligibilite_age = (age >= params.age.minimum) * (age <= params.age.maximum)

        quotient_familial = individu.foyer_fiscal(
            'rfr', period.n_2) / 12 / individu.foyer_fiscal('nbptr', period.n_2)
        eligibilite_quotient_familial = quotient_familial <= params.plafond_quotient_familial

        return allocataire_msa * eligibilite_geographique * eligibilite_age * eligibilite_quotient_familial * montant
