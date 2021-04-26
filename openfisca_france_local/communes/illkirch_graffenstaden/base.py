from openfisca_core.model_api import select
from openfisca_france.model.base import Famille, Individu, Menage, MONTH, Variable


class illkirch_graffenstaden_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs d'Illkirch Graffenstaden"

    def formula(menage, period):
        return menage('depcom', period) == b'67218'


class illkirch_graffenstaden_coupon_arts_et_sports_eligibilite_enfant(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité d'un enfant au coupon Arts et Sports"

    def formula(individu, period):
        return individu('age', period) < 18


class illkirch_graffenstaden_coupon_arts_et_sports_eligibilite_famille(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH
    label = "Éligibilité d'une famille au coupon Arts et Sports"

    def formula(famille, period):
        return famille.any(famille.members('illkirch_graffenstaden_coupon_arts_et_sports_eligibilite_enfant', period))


class illkirch_graffenstaden_coupon_arts_et_sports_quotient_familial(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Quotient familial pour le calcul du coupon Arts et Sports d'Illkirch Graffenstaden"

    def formula(famille, period):
      return famille.demandeur.foyer_fiscal('rfr', period.n_2) / 12 / famille.demandeur.foyer_fiscal('nbptr', period.n_2)


class illkirch_graffenstaden_coupon_arts_et_sports_montant(Variable):
    value_type = float
    entity = Famille
    label = "Montant pour une famille du coupon Arts et Sports du CCAS d'Illkirch Graffenstaden"
    definition_period = MONTH

    def formula(famille, period):
      qf = famille('illkirch_graffenstaden_coupon_arts_et_sports_quotient_familial', period)
      return 50 * select([
          qf <= 500,
          qf <= 600,
          qf <= 750
        ], [3, 2, 1],
        default=0
        )


class illkirch_graffenstaden_coupon_arts_et_sports(Variable):
    value_type = float
    entity = Famille
    label = "Montant pour une famille du coupon Arts et Sports du CCAS d'Illkirch Graffenstaden"
    reference = "http://www.illkirch.eu/wp-content/uploads/2020_CCAS_reglement_coupon-arts-et-sports.pdf"
    definition_period = MONTH

    def formula(famille, period):
      resid = famille.demandeur.menage('illkirch_graffenstaden_eligibilite_residence', period)
      fam_elig = famille('illkirch_graffenstaden_coupon_arts_et_sports_eligibilite_famille', period)
      montant = famille('illkirch_graffenstaden_coupon_arts_et_sports_montant', period)

      return resid * fam_elig * montant
