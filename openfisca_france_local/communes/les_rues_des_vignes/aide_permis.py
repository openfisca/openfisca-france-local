from openfisca_france.model.base import Variable, Individu, MONTH, TypesActivite


class les_rues_des_vignes_aide_mobilite_permis(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant de l'aide à la mobilité pour le permis de la ville de Les Rues-des-Vignes"
    reference = [
        "Règlement relatif à l’aide à la mobilité de la ville de Les Rues-des-Vignes",
        "https://www.lesruesdesvignes.fr/vie-pratique/demarches-administratives/aides-sociales"
        ]

    def formula(individu, period, parameters):
        age = individu('age', period)
        contrainte_age = parameters(period).communes.les_rues_des_vignes.aide_permis.age
        eligibilite_age = (contrainte_age.minimum <= age) * (age < contrainte_age.maximum)

        eligibilite_commune = individu.menage('depcom', period) == b"59517"
        eligibilite = eligibilite_age * eligibilite_commune

        montant = parameters(period).communes.les_rues_des_vignes.aide_permis.montant
        return montant * eligibilite
