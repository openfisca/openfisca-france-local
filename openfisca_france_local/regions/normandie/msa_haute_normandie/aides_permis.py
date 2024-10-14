from numpy.core.defchararray import startswith

from openfisca_france.model.base import Individu, MONTH, Variable
from openfisca_france.model.caracteristiques_socio_demographiques.demographie import RegimeSecuriteSociale

code_departements = [b'27', b'76']


class msa_haute_normandie_aide_permis(Variable):
    value_type = float
    entity = Individu
    label = "Éligibilité financière à l'aide à l’obtention du permis de conduire de la MSA Haute-Normandie"
    reference = "https://hautenormandie.msa.fr/lfy/aide-au-permis-de-conduire"
    definition_period = MONTH

    def formula(individu, period, parameters):
        params = parameters(period).regions.normandie.msa_haute_normandie.aide_permis
        ars_params = parameters(period).prestations_sociales.prestations_familiales.education_presence_parentale.ars.ars_plaf
        smic = parameters(period).marche_travail.salaire_minimum.smic

        montant = params.montant

        allocataire_msa = individu('regime_securite_sociale', period) == RegimeSecuriteSociale.regime_agricole
        enfant_a_charge = individu('enfant_a_charge', period.this_year)
        alternant = individu('alternant', period)

        depcom = individu.menage('depcom', period)
        eligibilite_geographique = sum([startswith(depcom, code_departement) for code_departement in code_departements])

        age = individu('age', period)
        eligibilite_age = (age >= params.age.minimum) * (age <= params.age.maximum)

        af_nbenf = individu.famille('af_nbenf', period)
        plafond_ressources = ars_params.plafond_ressources * (1 + af_nbenf * ars_params.majoration_par_enf_supp)
        eligibilite_plafond_ressources = individu.foyer_fiscal('rfr', period.n_2) <= plafond_ressources
        smic_brut_mensuel = smic.smic_b_horaire * smic.nb_heures_travail_mensuel
        eligibilite_salaire = individu('salaire_de_base', period) <= smic_brut_mensuel

        return (allocataire_msa + (enfant_a_charge * alternant)) * eligibilite_geographique * eligibilite_age * eligibilite_plafond_ressources * eligibilite_salaire * montant
