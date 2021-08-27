from openfisca_france.model.base import Variable, Individu, MONTH, TypesActivite


class le_cateau_aide_mobilite_permis(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant de l'aide à la mobilité pour le permis de la ville de Le Cateau"
    reference = [
        "Règlement relatif à l’aide à la mobilité de la ville de Le Cateau",
        "https://www.lecateau.fr/vivre-au-cateau/enfance-jeunesse/jeunesse/aide-au-permis-de-conduire.html"
        ]

    def formula(individu, period, parameters):
        age = individu('age', period)
        contrainte_age = parameters(period).communes.le_cateau.aide_permis.age
        eligibilite_age = (contrainte_age.minimum <= age) * (age <= contrainte_age.maximum)

        activite = individu('activite', period)
        eligibilite_activite = (activite == TypesActivite.chomeur) + (activite == TypesActivite.etudiant) + (activite == TypesActivite.inactif)

        eligibilite_commune = individu.menage('depcom', period) == b"59136"
        eligibilite =  eligibilite_age * eligibilite_activite * eligibilite_commune

        montant = parameters(period).communes.le_cateau.aide_permis.montant
        return montant * eligibilite
