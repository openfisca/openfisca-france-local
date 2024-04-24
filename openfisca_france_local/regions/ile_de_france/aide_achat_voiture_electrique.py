from openfisca_france.model.base import Individu, MONTH, Variable
from numpy.core.defchararray import startswith
from numpy import logical_not as not_

class ile_de_france_aide_achat_voiture_electrique(Variable):
    value_type = float
    entity = Individu
    label = "Aide à l'acquisition de voitures électriques"
    reference = "https://www.iledefrance.fr/aides-et-appels-a-projets/acquisition-de-vehicules-propres-par-les-particuliers"
    definition_period = MONTH

    def formula(individu, period, parameters):
        depcom = individu.menage('depcom', period)
        codes_departements = parameters(period).regions.ile_de_france.aide_achat_voiture_electrique.departements_eligibles
        eligibilite_geographique = sum([startswith(depcom, str.encode(code_departement)) for code_departement in codes_departements])

        codes_communes = parameters(period).regions.ile_de_france.aide_achat_voiture_electrique.codes_communes_non_eligibles
        exclusion_geographique = sum([depcom == str.encode(code_commune) for code_commune in codes_communes])

        rfr = individu.foyer_fiscal('rfr', period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period.n_2)
        quotient_familial = rfr / nbptr

        modalites = parameters(period).regions.ile_de_france.aide_achat_voiture_electrique.montant_en_fonction_du_quotient_familial
        montant = modalites.calc(quotient_familial)

        return montant * eligibilite_geographique * not_(exclusion_geographique)
