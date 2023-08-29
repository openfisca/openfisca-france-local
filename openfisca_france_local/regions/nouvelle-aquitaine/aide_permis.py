from openfisca_france.model.base import Variable, Individu, MONTH, TypesActivite, set_input_dispatch_by_period
from openfisca_france.model.caracteristiques_socio_demographiques.logement import (TypesCodeInseeRegion)
from openfisca_france.model.prestations.education import TypesScolarite


class service_civique(Variable):
    # A supprimer une fois intégrée à openfisca-france
    value_type = bool
    label = 'En service civique'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = 'https://www.service-public.fr/particuliers/vosdroits/F13278'


class nouvelle_aquitaine_aide_permis(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    reference = 'https://les-aides.nouvelle-aquitaine.fr/amenagement-du-territoire/aide-au-passage-du-permis-de-conduire-b'

    def formula(individu, period, parameters):
        params = parameters(period).regions.nouvelle_aquitaine.aide_permis

        region_residence = individu.menage('region', period)
        eligibilite_geographique = sum([region_residence == TypesCodeInseeRegion.nouvelle_aquitaine])

        age = individu('age', period)
        age_minimum = params.age.minimum_inclusif
        age_maximum = params.age.maximum_inclusif
        eligibilite_age = (age >= age_minimum) * (age <= age_maximum)

        activite = individu('activite', period)
        est_lyceen = individu('scolarite', period) == TypesScolarite.lycee

        est_chomeur = activite == TypesActivite.chomeur

        est_alternant = individu('alternant', period)

        en_service_civique = individu('service_civique', period)

        eligibilite_profile = est_chomeur + est_lyceen + en_service_civique + est_alternant

        montant = (700 * est_alternant) + (1200 * (1 - est_alternant))

        return montant * eligibilite_geographique * eligibilite_age * eligibilite_profile
