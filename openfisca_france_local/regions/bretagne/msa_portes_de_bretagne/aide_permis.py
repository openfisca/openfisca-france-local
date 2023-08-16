from numpy.core.defchararray import startswith

from openfisca_france.model.base import Individu, MONTH, Variable, ADD
from openfisca_france.model.caracteristiques_socio_demographiques.demographie import RegimeSecuriteSociale

code_departements = [b'35', b'56']


class msa_portes_de_bretagne_aide_permis(Variable):
    value_type = float
    entity = Individu
    label = "Éligibilité financière à l'aide à l’obtention du permis de conduire de la MSA Portes de Bretagne"
    reference = "https://portesdebretagne.msa.fr/lfy/aide-au-permis-de-conduire"
    definition_period = MONTH

    def formula(individu, period, parameters):
        params = parameters(period).regions.bretagne.msa_portes_de_bretagne.aide_permis

        montant = params.montant

        depcom = individu.menage('depcom', period)
        eligibilite_geographique = sum([startswith(depcom, code_departement) for code_departement in code_departements])

        allocataire_msa = individu('regime_securite_sociale', period) == RegimeSecuriteSociale.regime_agricole

        age = individu('age', period)
        eligibilite_age = age <= params.age.maximum

        smic = parameters(period).marche_travail.salaire_minimum.smic
        smic_brut_mensuel = smic.smic_b_horaire * smic.nb_heures_travail_mensuel
        eligibilite_salaire = individu('salaire_de_base', period.last_3_months, options = [ADD]) / 3 / smic_brut_mensuel * 100 <= params.pourcentage_ressources_maximum_jeune

        quotient_familial = individu.foyer_fiscal(
            'rfr', period.n_2) / 12 / individu.foyer_fiscal('nbptr', period.n_2)
        enfant_a_charge = individu('enfant_a_charge', period.this_year)
        eligibilite_famillle = (quotient_familial <= params.plafond_quotient_familial) * enfant_a_charge


        return eligibilite_geographique * allocataire_msa * eligibilite_age * (eligibilite_salaire + eligibilite_famillle) * montant
