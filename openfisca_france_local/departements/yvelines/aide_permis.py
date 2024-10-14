from openfisca_france.model.base import Variable, Individu, MONTH


class yvelines_aide_permis(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant de l'aide au permis de conduire pour le département des Yvelines"
    reference = 'https://www.78-92.fr/annuaire/aides-et-services/detail/laide-au-financement-du-permis-de-conduire'

    def formula(individu, period, parameters):
        params = parameters(period).departements.yvelines.aide_permis

        individus_age = individu('age', period)

        age_maximum = params.age.maximum_inclusif
        age_minimum = params.age.minimum_inclusif
        eligibilites_age = (individus_age >= age_minimum) * (individus_age <= age_maximum)

        eligibilite_residentielle = individu.menage('yvelines_eligibilite_residence', period)

        rbg = individu.foyer_fiscal('rbg', period.n_2)
        nb_pac = individu.foyer_fiscal('nb_pac', period.n_2)

        rbg_max = params.revenu_global_brut.base + (nb_pac * params.revenu_global_brut.marginal_par_personne)
        eligibilite_revenu = rbg < rbg_max

        montant = params.montant

        return eligibilites_age * eligibilite_residentielle * eligibilite_revenu * montant
