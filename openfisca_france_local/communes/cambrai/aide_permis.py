from openfisca_france.model.base import Variable, Individu, MONTH, TypesActivite


class cambrai_aide_mobilite_permis_b(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant de l'aide à la mobilité pour le permis B de la ville de Cambrai"
    reference = [
        "Règlement relatif à l’aide à la mobilité de la ville de Cambrai",
        "https://www.villedecambrai.com/jeunesse/bourses-et-aides/aide-au-permis-de-conduire"
        ]

    def formula(individu, period, parameters):
        age = individu('age', period)
        contrainte_age = parameters(period).communes.cambrai.aide_permis.age
        eligibilite_age = (contrainte_age.minimum <= age) * (age <= contrainte_age.maximum)

        activite = individu('activite', period)
        eligibilite_activite = (activite == TypesActivite.chomeur) + (activite == TypesActivite.etudiant) + (activite == TypesActivite.inactif)

        eligibilite_commune = individu.menage('depcom', period) == b"59122"
        eligibilite = eligibilite_age * eligibilite_activite * eligibilite_commune

        montant = parameters(period).communes.cambrai.aide_permis.montant
        return montant * eligibilite
