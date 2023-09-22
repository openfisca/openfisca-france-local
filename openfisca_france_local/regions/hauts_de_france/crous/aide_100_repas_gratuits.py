from numpy.core.defchararray import startswith
from openfisca_france.model.prestations.education import TypesScolarite, TypesClasse
from openfisca_france.model.base import Individu, MONTH, not_, Variable

code_departements = [b'59', b'62']

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
        depcom = individu.menage('depcom', period)
        anne_etude = individu('annee_etude', period)
        echelon_boursier = individu('bourse_criteres_sociaux_echelon', period)

        
        eligibilite_geographique = sum([startswith(depcom, code_departement) for code_departement in code_departements])

        # Sont éligibles les étudiants ayant moins de 35 ans (limite d’âge non applicable aux étudiants en situation de handicap)
        eligibilite_age = not_(handicap) * (age <= params.age.maximum) + handicap

        # Sont éligibles les personnes inscrites dans un établissement d’enseignement supérieur, public ou privé, partenaire de la Région, reconnu par le ministère de l’Enseignement supérieur, 
        # de la recherche et de l’innovation sur le territoire des Hauts-de-France, ou inscrites dans un établissement dispensant une formation sanitaire ou sociale gérée par la Région.
        eligibilite_scolarite = (individu('scolarite', period) == TypesScolarite.enseignement_superieur) # + (individu('scolarite', period) == TypesScolarite.formation_sanitaire_ou_sociale) @Todo : Ajouter la variable 'formation_sanitaire_ou_sociale' sur sur openfisca-france ? 

        # Sont éligibles les étudiants inscrits en BTS sont exclus de ce dispositif ainsi que tous les étudiants dont l’établissement d’inscription est un lycée, tels que les étudiants en CPGE. 
        eligibilite_annee_etude = (anne_etude != TypesClasse.cpge_1) * (anne_etude != TypesClasse.bts_1) * (anne_etude != TypesClasse.bts_2) * (anne_etude != TypesClasse.cpge_2)

        # Sont éligibles les étudiants boursiers échelon 3 à 7
        eligiblite_echelon_boursier = (echelon_boursier >= params.echelon_boursier.minimum ) * (echelon_boursier <= params.echelon_boursier.maximum)

        return eligibilite_geographique * eligibilite_age * eligibilite_scolarite * eligibilite_annee_etude * eligiblite_echelon_boursier
 