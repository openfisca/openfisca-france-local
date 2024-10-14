
from openfisca_france.model.base import (
    Variable, Individu, MONTH, TypesActivite)


class sous_contrat_engagement_jeune(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Est actuellement en Contrat Engagement Jeune"


class revenu_solidaire_jeune(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant du Revenu Solidaire Jeune"
    reference = 'https://aides-jeunes.grandlyon.com/#c21886'

    def formula(individu, period, parameter):
        modalites = parameter(period).metropoles.lyon.revenu_solidaire_jeune
        age = individu('age', period)
        eligibilite_age = (age >= modalites.age.minimum_inclusif) * (age <= modalites.age.maximum_inclusif)

        reside_metropole_lyon = individu.menage('lyon_metropole_eligibilite_geographique', period)

        rsa = individu.famille('rsa', period)
        aah = individu('aah', period)
        aeeh = individu.famille('aeeh', period)
        sous_contrat_engagement_jeune = individu('sous_contrat_engagement_jeune', period)
        prestations_incompatibles = rsa + aah + aeeh + sous_contrat_engagement_jeune
        eligibilite_prestations = prestations_incompatibles == 0

        pas_en_etude = individu('activite', period) != TypesActivite.etudiant

        revenus_activite = (
            individu('salaire_net', period)
            + individu('indemnites_stage', period)
            + individu.famille('ppa', period)
            + individu('revenus_stage_formation_pro', period)
            )

        montant = modalites.montant.calc(revenus_activite)

        return montant * eligibilite_age * reside_metropole_lyon * eligibilite_prestations * pas_en_etude
