from openfisca_france.model.base import Variable, MONTH, Famille, TypesActivite

class auvergne_mutuelle_communale_etudiant(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH
    label = "Mutuelle communale de la région Auvergne Rhône Alpes pour les étudiants"
    reference = [
        "https://www.auvergnerhonealpes.fr/particuliers/mutuelleetudiants"
        ]

    def formula(famille, period, parameters):
        params = parameters(period).regions.auvergne_rhone_alpes.auvergne_mutuelle_communale_etudiant
        auvergne_mutuelle_communale = famille('auvergne_mutuelle_communale_base', period)
        eligibilite_etudiant = (
                famille.demandeur('activite', period) == TypesActivite.etudiant)

        age = famille.demandeur('age', period)
        eligibilite_age = (age >= params.age.minimum) * (age <= params.age.maximum)

        return eligibilite_etudiant * eligibilite_age * auvergne_mutuelle_communale
