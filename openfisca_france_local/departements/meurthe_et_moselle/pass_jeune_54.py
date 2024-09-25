from openfisca_france.model.base import Variable, Individu, MONTH


class eligibilite_age_pass_jeune_54(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité d'âge pour le Pass Jeune 54 du département Meurthe-et-Moselle"

    def formula(individu, period, parameters):
        age = individu('age', period)
        age_minimum = parameters(period).departements.meurthe_et_moselle.pass_jeune_54.age.minimum_inclusif
        age_maximum = parameters(period).departements.meurthe_et_moselle.pass_jeune_54.age.maximum_inclusif
        return (age_minimum <= age) * (age <= age_maximum)

class quotient_familial_pass_jeune_54(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Quotient familial pour le Pass Jeune 54 du département Meurthe-et-Moselle"

    def formula(individu, period):
        rfr = individu.foyer_fiscal('rfr', period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period.n_2)
        return rfr / nbptr / 12

class pass_jeune_54(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant pour le Pass Jeune 54 du département Meurthe-et-Moselle"
    reference = [
        "https://meurthe-et-moselle.fr/actions/education-populaire-jeunesse-sports/sport/pass-jeunes-54"
        ]

    def formula(individu, period, parameters):

        params = parameters(period).departements.meurthe_et_moselle.pass_jeune_54

        eligibilite_residentielle = individu.menage('meurthe_et_moselle_eligibilite_residence', period)
        eligibilite_age = individu('eligibilite_age_pass_jeune_54', period)
        quotient_familial = individu('quotient_familial_pass_jeune_54', period)

        montant = params.montant_en_fonction_du_quotient_familial.calc(quotient_familial)

        return montant * eligibilite_residentielle * eligibilite_age
