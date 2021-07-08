from openfisca_france.model.base import Variable, Individu, MONTH, TypesActivite


class cambrai_aide_mobilite_permis_b_eligibilite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité d'âge pour l'aide à la mobilité pour le permis B de la ville de Cambrai"

    def formula(individu, period):
        age = individu('age', period)
        activite = individu('activite', period)
        eligibilite_age = (18 <= age) * (age <= 25)
        eligibilite_type = (activite == TypesActivite.chomeur) + (activite == TypesActivite.etudiant) + (activite == TypesActivite.inactif)
        eligibilite_commune = individu.menage('depcom', period) == b"59122"
        return eligibilite_age * eligibilite_type * eligibilite_commune


class cambrai_aide_mobilite_permis_b(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant de l'aide à la mobilité pour le permis B de la ville de Cambrai"
    reference = [
        "Règlement relatif à l’aide à la mobilité",
        "https://www.villedecambrai.com/jeunesse/bourses-et-aides/aide-au-permis-de-conduire"
        ]

    def formula(individu, period, parameters):
        montant = parameters(period).communes.cambrai.aide_permis.montant
        return montant * individu('cambrai_aide_mobilite_permis_b_eligibilite', period)
