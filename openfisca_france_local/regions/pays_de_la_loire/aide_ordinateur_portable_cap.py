from openfisca_france.model.base import Variable, Individu, MONTH, TypesNiveauDiplome
from openfisca_france.model.prestations.education import TypesClasse
from numpy.core.defchararray import startswith
import numpy as np


CODE_DEPARTEMENTS_PAYS_DE_LA_LOIRE = [b'44', b'49', b'53', b'72', b'85']


class eligibilite_aide_ordinateur_portable_cap_pays_de_la_loire(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Elligibilité à la fourniture d'un ordinateur portable aux élèves de CAP par la région des Pays de la Loire"
    reference = [
        "https://www.paysdelaloire.fr/jeunesse-et-education/un-ordinateur-portable-fourni-par-la-region-aux-eleves-de-seconde-et-1ere-annee-de-cap"
        ]

    def formula(individu, period):
        eligibilite_region = np.any(startswith(individu.menage('depcom', period), code_postal) for code_postal in CODE_DEPARTEMENTS_PAYS_DE_LA_LOIRE)
        eligibilite_annee_etude = (individu('annee_etude', period) == TypesClasse.seconde) + (individu('annee_etude', period) == TypesClasse.premiere)
        eligibilite_niveau_diplome_formation = individu('niveau_diplome_formation', period) == TypesNiveauDiplome.niveau_3
        return eligibilite_region * eligibilite_annee_etude * eligibilite_niveau_diplome_formation
