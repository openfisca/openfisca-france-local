from openfisca_france.model.base import MONTH, Variable, TypesActivite, Famille
from openfisca_france.model.caracteristiques_socio_demographiques.logement import (
    TypesCodeInseeRegion)


class hauts_de_france_aide_garde_enfant(Variable):
    value_type = float
    entity = Famille
    label = "Éligibilité financière à l'Aide à la Garde d'Enfant (AGE)"
    reference = [
        'https://www.hautsdefrance.fr/aide-garde-enfant/',
        'https://guide-aides.hautsdefrance.fr/aide636'
    ]
    definition_period = MONTH

    def formula(famille, period, parameters):
        modalites = parameters(
            period).regions.hauts_de_france.aide_garde_enfant
        couple = famille('en_couple', period)
        montant = (modalites.montant.famille_monoparentale * (1 - couple)
                   ) + (modalites.montant.famille_biparentale * couple)

        age = famille.members('age', period)
        enfants_eligibles = (age < modalites.age_maximum_enfant)
        montant_par_enfant = montant * enfants_eligibles
        montant_total = famille.sum(montant_par_enfant, role=Famille.ENFANT)

        region = famille.demandeur.menage('region', period)
        eligibilite_geographique = sum(
            [region == TypesCodeInseeRegion.hauts_de_france])

        actifs = famille.members('activite', period) == TypesActivite.actif
        nombre_parents = famille.nb_persons(role=Famille.PARENT)
        eligibilite_statut = famille.sum(
            actifs, role=Famille.PARENT) == nombre_parents

        plafond_param = modalites.plafond_multiple_smic
        plafond_ressources_smic = (plafond_param.famille_monoparentale * (
            1 - couple)) + (plafond_param.famille_biparentale * couple)
        smic = parameters(
            period).marche_travail.salaire_minimum.smic.smic_b_mensuel

        rni = famille.demandeur.foyer_fiscal('rni', period.this_year)
        eligibilite_revenus = rni/12 < plafond_ressources_smic * smic
        return montant_total * eligibilite_geographique * eligibilite_statut * eligibilite_revenus
