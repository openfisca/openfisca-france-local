from openfisca_france.model.base import Variable, Individu, MONTH


class haute_vienne_aide_permis(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant de l'aide au permis de conduire pour le département de la Haute-Vienne"
    reference = 'https://www.haute-vienne.fr/nos-actions/jeunesse/besoin-dun-coup-de-pouce/aide-au-permis-de-conduire'

    def formula(individu, period, parameters):
        params = parameters(period).departements.haute_vienne.aide_permis

        individus_age = individu('age', period)

        age_maximum = params.age.maximum_exclusif
        age_minimum = params.age.minimum_inclusif
        age_eligibilites = (individus_age >= age_minimum) * (individus_age < age_maximum)

        eligibilite_residentielle = individu.menage('haute_vienne_eligibilite_residence', period)

        rfr = individu.foyer_fiscal('rfr', period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period.n_2)
        quotient_familial = rfr / nbptr / 12
        montant = params.montant_en_fonction_du_quotient_familial.calc(quotient_familial)

        return age_eligibilites * eligibilite_residentielle * montant
