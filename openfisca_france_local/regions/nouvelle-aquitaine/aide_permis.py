
from openfisca_france.model.base import (
    Variable, Individu, MONTH, TypesActivite, select, not_)
from openfisca_france.model.caracteristiques_socio_demographiques.logement import (TypesCodeInseeRegion)
from openfisca_france.model.prestations.education import TypesScolarite, TypesClasse


class eligibilite_age_nouvelle_aquitaine_aide_permis(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité d'âge de l'aide au permis de la région Nouvelle-Aquitaine"

    def formula(individu, period, parameters):
        modalites_age = parameters(period).regions.nouvelle_aquitaine.aide_permis.age
        age = individu('age', period)
        age_minimum = modalites_age.minimum_inclusif
        age_maximum = modalites_age.maximum_inclusif
        return (age >= age_minimum) * (age <= age_maximum)


class eligibilite_profile_nouvelle_aquitaine_aide_permis(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité de situation de l'aide au permis de la région Nouvelle-Aquitaine"

    def formula(individu, period):
        est_chomeur = individu('activite', period) == TypesActivite.chomeur

        est_lyceen = individu('scolarite', period) == TypesScolarite.lycee
        annee_etude = individu('annee_etude', period)
        eligibilite_annee_etude = ((annee_etude == TypesClasse.cap_2) + (annee_etude == TypesClasse.terminale)) * (est_lyceen)

        est_alternant = individu('alternant', period)

        en_service_civique = individu('service_civique', period)

        return est_chomeur + eligibilite_annee_etude + en_service_civique + est_alternant


class montant_nouvelle_aquitaine_aide_permis(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant de l'aide au permis de la région Nouvelle-Aquitaine"

    def formula(individu, period, parameters):
        modalites_montants = parameters(period).regions.nouvelle_aquitaine.aide_permis
        rfr = individu.foyer_fiscal('rfr', period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period.n_2)
        quotient_familial = rfr / nbptr

        est_alternant = individu('alternant', period)

        calcul_montant_alternants = modalites_montants.montant_en_fonction_du_quotient_familial_pour_alternants.calc
        calcul_montant = modalites_montants.montant_en_fonction_du_quotient_familial.calc
        return select([est_alternant, not_(est_alternant)],
                    [calcul_montant_alternants(quotient_familial), calcul_montant(quotient_familial)])


class nouvelle_aquitaine_aide_permis(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    reference = 'https://les-aides.nouvelle-aquitaine.fr/amenagement-du-territoire/aide-au-passage-du-permis-de-conduire-b'
    label = "Éligibilité et montant associé de l'aide au permis de la région Nouvelle-Aquitaine"
    documentation = '''
    La modélisation de cette aide ne correspond pas à la réalité.
    Les conditions décrites dans le paragraphe `Diplômé de la filière professionnelle ou agricole en insertion professionnelle` sont modélisées en fonction des profils susceptibles d'être intéressés lors d'une simulation avec Aides-Jeunes.

    De plus, les profils décrits dans les paragraphes suivants ne sont pas modélisés :
    - En insertion professionnelle suivi par une mission locale
    - Scolarisé en établissement régional d’enseignement adapté (EREA)
    '''

    def formula(individu, period):
        region_residence = individu.menage('region', period)
        eligibilite_geographique = sum([region_residence == TypesCodeInseeRegion.nouvelle_aquitaine])

        eligibilite_age = individu('eligibilite_age_nouvelle_aquitaine_aide_permis', period)

        eligibilite_profile = individu('eligibilite_profile_nouvelle_aquitaine_aide_permis', period)

        montant = individu('montant_nouvelle_aquitaine_aide_permis', period)

        return montant * eligibilite_geographique * eligibilite_age * eligibilite_profile
