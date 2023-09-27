from numpy.core.defchararray import startswith
from openfisca_france.model.prestations.education import TypesScolarite, TypesClasse
from openfisca_france.model.caracteristiques_socio_demographiques.logement import TypesCodeInseeRegion
from openfisca_france.model.base import Individu, MONTH, not_, Variable
from openfisca_france.model.caracteristiques_socio_demographiques.demographie import GroupeSpecialitesFormation
class crous_aide_100_repas_gratuits(Variable):
    value_type = float
    entity = Individu
    label = "Éligibilité financière à l'aide du crous et de la région Hauts-de-France de 100 repas gratuits aux étudiants boursiers échelon 3 à 7"
    reference = "https://www.ij-hdf.fr/actualite/747/100-repas-gratuits-de-nouveau-attribues-aux-etudiants-boursiers-echelon-3-a-7#:~:text=Le%20Conseil%20R%C3%A9gional%20Hauts-de,en%20restos"
    definition_period = MONTH

    def formula(individu, period, parameters):
        params = parameters(period).regions.hauts_de_france.crous.aide_100_repas_gratuits

        age = individu('age', period)
        handicap = individu('handicap', period)
        region = individu.menage('region', period)
        scolarite = individu('scolarite', period)
        annee_etude = individu('annee_etude', period)
        echelon_boursier = individu('bourse_criteres_sociaux_echelon', period)
        groupe_specialites_formation = individu('groupe_specialites_formation', period)

        eligibilite_geographique = (region == TypesCodeInseeRegion.hauts_de_france)

        eligibilite_age = (age <= params.age.maximum) + handicap

        eligibilite_scolarite_formation = (scolarite  == TypesScolarite.enseignement_superieur) + (groupe_specialites_formation == GroupeSpecialitesFormation.groupe_330)

        eligibilite_annee_etude = (annee_etude != TypesClasse.cpge_1) * (annee_etude != TypesClasse.bts_1) * (annee_etude != TypesClasse.bts_2) * (annee_etude != TypesClasse.cpge_2)

        eligiblite_echelon_boursier = (echelon_boursier >= params.echelon_boursier.minimum ) * (echelon_boursier <= params.echelon_boursier.maximum)

        return eligibilite_geographique * eligibilite_age * eligibilite_scolarite_formation * eligibilite_annee_etude * eligiblite_echelon_boursier
