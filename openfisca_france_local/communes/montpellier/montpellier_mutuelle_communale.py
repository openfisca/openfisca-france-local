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
        css_participation_forfaitaire = famille('css_participation_forfaitaire_montant', period)
        eligibilite_css = css_participation_forfaitaire > 0
        return eligibilite_residentielle & not_(eligibilite_css)
