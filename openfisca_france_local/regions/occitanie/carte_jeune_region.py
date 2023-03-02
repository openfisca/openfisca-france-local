from openfisca_france.model.base import Variable, Individu, MONTH, TypesActivite
from openfisca_france.model.prestations.education import TypesClasse, StatutsEtablissementScolaire
from openfisca_france.model.caracteristiques_socio_demographiques.logement\
    import TypesCodeInseeRegion


class occitanie_carte_jeune_region(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Eligibilité à la Carte Jeune Région"
    reference = [
        "https://www.laregion.fr/cartejeune",
        "https://www.laregion.fr/la-carte-jeune-region-c-est-quoi-35189"
    ]

    def formula(individu, period):
        region = individu.menage('region', period)
        occitanie_eligibilite_residence = (
            region == TypesCodeInseeRegion.occitanie)

        eligibilite_etudiant = (
            individu('activite', period) == TypesActivite.etudiant)

        annee_etude = individu('annee_etude', period)
        eligibilite_annee_etude = (annee_etude == TypesClasse.seconde) + \
                                  (annee_etude == TypesClasse.premiere) + \
                                  (annee_etude == TypesClasse.terminale) + \
                                  (annee_etude == TypesClasse.bts_1) + \
                                  (annee_etude == TypesClasse.bts_2) + \
                                  (annee_etude == TypesClasse.cpge_1) + \
                                  (annee_etude == TypesClasse.cpge_2)

        statuts_etablissement_scolaire = individu(
            'statuts_etablissement_scolaire', period)
        eligibilite_statuts_etablissement_scolaire = (
            statuts_etablissement_scolaire == StatutsEtablissementScolaire.public) + (
            statuts_etablissement_scolaire == StatutsEtablissementScolaire.prive_sous_contrat)

        return occitanie_eligibilite_residence * eligibilite_annee_etude * eligibilite_etudiant * eligibilite_statuts_etablissement_scolaire
