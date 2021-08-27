from openfisca_france.model.base import Variable, Individu, MONTH, TypesActivite


class iwuy_aide_mobilite_permis(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant de l'aide à la mobilité pour le permis de la ville de Iwuy"
    reference = [
        "Règlement relatif à l’aide à la mobilité de la ville de Iwuy",
        "http://www.iwuy.fr/page.php?id=6#39"
        ]

    def formula(individu, period, parameters):
        age = individu('age', period)
        contrainte_age = parameters(period).communes.iwuy.aide_permis.age
        eligibilite_age = (contrainte_age.minimum <= age) * (age < contrainte_age.maximum)

        eligibilite_commune = individu.menage('depcom', period) == b"59322"
        eligibilite = eligibilite_age * eligibilite_commune

        montant = parameters(period).communes.iwuy.aide_permis.montant
        return montant * eligibilite
