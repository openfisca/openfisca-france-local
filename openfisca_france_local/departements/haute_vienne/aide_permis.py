from openfisca_france.model.base import Variable, Individu, MONTH


class haute_vienne_aide_permis(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant de l'aide au permis de conduire pour le département de la Haute-Vienne"
    reference = 'https://www.haute-vienne.fr/nos-actions/jeunesse/besoin-dun-coup-de-pouce/aide-au-permis-de-conduire'

    def formula(individu, period, parameters):
        individus_age = individu('age', period)

        age_eligibilites = (individus_age >= 15) * (individus_age < 25)

        return age_eligibilites
