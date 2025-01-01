from openfisca_france.model.base import Variable, MONTH, not_, Famille, TypesActivite
from openfisca_france.model.caracteristiques_socio_demographiques.logement \
    import TypesCodeInseeRegion

class auvergne_mutuelle_communale_base(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH
    label = "Mutuelle communale de la région Auvergne Rhône Alpes - éligibilité de base"
    reference = [
        "https://www.auvergnerhonealpes.fr/particuliers/mamutuelleregion"
        ]

    def formula(famille, period):
        region = famille.demandeur.menage('region', period)
        eligibilite_residentielle = (
                region == TypesCodeInseeRegion.auvergne_rhone_alpes)
        css_participation_forfaitaire = famille('css_participation_forfaitaire', period)
        cmu_c = famille('cmu_c', period)
        eligibilite_css_cmu_c = (css_participation_forfaitaire > 0) | cmu_c
        return eligibilite_residentielle * not_(eligibilite_css_cmu_c)

class auvergne_mutuelle_communale(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH
    label = "Mutuelle communale de la région Auvergne Rhône Alpes (hors étudiants)"
    reference = [
        "https://www.auvergnerhonealpes.fr/particuliers/mamutuelleregion"
        ]

    def formula(famille, period):
        auvergne_mutuelle_communale_base = famille('auvergne_mutuelle_communale_base', period)
        etudiant = (
                famille.demandeur('activite', period) == TypesActivite.etudiant)
        return auvergne_mutuelle_communale_base * not_(etudiant)
