
from openfisca_france.model.base import (
    Variable, Individu, MONTH, TypesActivite)


class revenu_solidaire_jeune(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant du Revenu Solidaire Jeune"
    reference = 'https://aides-jeunes.grandlyon.com/#c21886'

    def formula(individu, period, parameter):
        age_eligibles = parameter(period).metropoles.lyon.revenu_solidaire_jeune.age
        age = individu('age', period)
        eligibilite_age = (age >= age_eligibles.minimum_inclusif) * (age <= age_eligibles.maximum_inclusif)

        reside_metropole_lyon = individu.menage('lyon_metropole_eligibilite_geographique', period)

        rsa = individu.famille('rsa', period)
        aah = individu('aah', period)
        aeeh = individu.famille('aeeh', period)
        contrat_engagement_jeune = individu('contrat_engagement_jeune', period)
        prestations_incompatibles = rsa + aah + aeeh + contrat_engagement_jeune
        eligibilite_prestations = prestations_incompatibles == 0

        pas_en_etude = individu('activite', period) != TypesActivite.etudiant

        return 420 * eligibilite_age * reside_metropole_lyon * eligibilite_prestations * pas_en_etude
