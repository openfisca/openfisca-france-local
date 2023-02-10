from openfisca_france.model.base import MONTH, Variable, TypesActivite, Famille
from openfisca_france.model.base import *
from openfisca_france.model.caracteristiques_socio_demographiques.logement import (
    TypesCodeInseeRegion)

code_departements = [b'02', b'59', b'60', b'62', b'80']


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
        params = parameters(period).regions.hauts_de_france.aide_garde_enfant
        couple = famille('en_couple', period)
        montant = (params.montant.famille_monoparentale * (1 - couple)
                   ) + (params.montant.famille_biparentale * couple)

        age = famille.members('age', period)
        enfants_eligibles = (age < params.age_maximum_enfant)
        montant_par_enfant = montant * enfants_eligibles
        montant_total = famille.sum(montant_par_enfant, role=Famille.ENFANT)

        region = famille.demandeur.menage('region', period)
        eligibilite_geographique = sum(
            [region == TypesCodeInseeRegion.hauts_de_france])

        actifs = famille.members('activite', period) == TypesActivite.actif
        nombre_parents = famille.nb_persons(role=Famille.PARENT)
        eligibilite_statut = famille.sum(
            actifs, role=Famille.PARENT) == nombre_parents

        plafond_ressources = params.plafond_ressources
        rfr = famille.demandeur.foyer_fiscal('rfr', period.this_year)
        eligibilite_revenus = rfr < plafond_ressources

        return montant_total * eligibilite_geographique * eligibilite_statut * eligibilite_revenus
