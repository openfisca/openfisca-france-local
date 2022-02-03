from numpy.core.defchararray import startswith

from openfisca_france.model.base import *
from openfisca_france.model.revenus.activite.salarie import TypesContrat


code_departements = [b'02', b'59', b'60', b'62', b'80']


class hauts_de_france_aide_permis_eligibilite(Variable):
    value_type = bool
    entity = Individu
    reference = [
        "https://www.hautsdefrance.fr/aide-au-permis-de-conduire/",
        "https://www.hautsdefrance.fr/permis-de-conduire-aide-2/"
    ]
    label = "Éligibilité financière à l'aide à l’obtention du permis de conduire"
    definition_period = MONTH
    documentation = '''
    Conditions non-modélisées :
        - demandeur dans un parcours contractualisé d’accompagnement vers l’emploi et l’autonomie (PACEA)
    '''

    def formula(individu, period, parameters):
        age = individu('age', period)
        criteres_age = parameters(period).regions.hauts_de_france.aide_permis.age
        eligibilite_age = (criteres_age.minimum <= age) * (age <= criteres_age.maximum)

        depcom = individu.menage('depcom', period)
        eligibilite_geographique = sum([startswith(depcom, code_departement) for code_departement in code_departements])

        plafond_ressources = parameters(period).regions.hauts_de_france.aide_permis.plafond_ressources
        rfr = individu.foyer_fiscal('rfr', period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period.n_2)

        activite_eligible = (individu('activite', period) == TypesActivite.chomeur) + (individu('activite', period) == TypesActivite.inactif) + (individu('activite', period) == TypesActivite.etudiant)
        en_cdd = individu('contrat_de_travail_type', period) == TypesContrat.cdd
        stagiaire = individu('stagiaire', period)
        eligibilite_situation = activite_eligible + en_cdd + stagiaire

        statut_marital = individu('statut_marital', period)
        eligibilite_couple = (
            ((statut_marital == TypesStatutMarital.marie) + (statut_marital == TypesStatutMarital.pacse)) *
            plafond_ressources.base_personne_couple >= rfr
        )
        eligibilite_autonome = (
            (statut_marital == TypesStatutMarital.celibataire) *
            plafond_ressources.base_personne_autonome >= max_(0, rfr / nbptr)
        )

        return eligibilite_age * eligibilite_geographique * eligibilite_situation * (eligibilite_autonome + eligibilite_couple)

    def formula_2021_07_21(individu, period, parameters):
        age = individu('age', period)
        criteres_age = parameters(period).regions.hauts_de_france.aide_permis.age
        eligibilite_age = (criteres_age.minimum <= age) * (age <= criteres_age.maximum)

        depcom = individu.menage('depcom', period)
        eligibilite_geographique = sum([startswith(depcom, code_departement) for code_departement in code_departements])

        plafond_ressources = parameters(period).regions.hauts_de_france.aide_permis.plafond_ressources
        rfr = individu.foyer_fiscal('rfr', period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period.n_2)

        activite_eligible = (individu('activite', period) == TypesActivite.chomeur) + (individu('activite', period) == TypesActivite.inactif)
        stagiaire = individu('stagiaire', period)
        apprenti = individu('apprenti', period)
        eligibilite_situation = activite_eligible + stagiaire + apprenti

        statut_marital = individu('statut_marital', period)
        eligibilite_couple = (
            ((statut_marital == TypesStatutMarital.marie) + (statut_marital == TypesStatutMarital.pacse)) *
            plafond_ressources.base_personne_couple >= rfr
        )
        eligibilite_autonome = (
            (statut_marital == TypesStatutMarital.celibataire) *
            plafond_ressources.base_personne_autonome >= max_(0, rfr / nbptr)
        )

        return eligibilite_age * eligibilite_geographique * eligibilite_situation * (eligibilite_autonome + eligibilite_couple)


class hauts_de_france_aide_permis(Variable):
    value_type = float
    entity = Individu
    label = "Éligibilité financière à l'aide à l’obtention du permis de conduire"
    reference = [
        "https://www.hautsdefrance.fr/aide-au-permis-de-conduire/"
    ]
    definition_period = MONTH

    def formula(individu, period, parameters):
        eligibilite = individu("hauts_de_france_aide_permis_eligibilite", period)
        montant = parameters(period).regions.hauts_de_france.aide_permis.montant
        return eligibilite * montant
