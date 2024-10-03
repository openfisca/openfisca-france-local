from openfisca_france.model.base import Variable, MONTH, not_, Famille

class montpellier_mutuelle_communale(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH
    label = "Mutuelle communale de la ville de Montpellier"
    reference = [
        "https://www.montpellier.fr/4884-mutuelle-communale.htm"
        ]

    def formula(famille, period):
        eligibilite_residentielle = famille.demandeur.menage('montpellier_eligibilite_residence', period)
        css_participation_forfaitaire = famille('css_participation_forfaitaire', period)
        cmu_c = famille('cmu_c', period)
        eligibilite_css_cmu_c = (css_participation_forfaitaire > 0) | cmu_c
        return eligibilite_residentielle * not_(eligibilite_css_cmu_c)
