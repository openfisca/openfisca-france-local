from openfisca_france.model.base import Variable, Individu, MONTH
from openfisca_france.model.prestations.education\
    import StatutsEtablissementScolaire, TypesScolarite
from openfisca_france.model.caracteristiques_socio_demographiques.logement\
    import TypesCodeInseeRegion


class occitanie_carte_transport_scolaire_lio(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Eligibilité à la carte de transport scolaire liO"
    reference = "https://lio.laregion.fr/transport-scolaire"

    def formula(individu, period):
        region = individu.menage('region', period)
        occitanie_eligibilite_residence = (
            region == TypesCodeInseeRegion.occitanie)

        scolarite = individu('scolarite', period)
        eligibilite_scolarite = (scolarite == TypesScolarite.maternelle) + \
                                (scolarite == TypesScolarite.primaire) + \
                                (scolarite == TypesScolarite.college) + \
                                (scolarite == TypesScolarite.lycee)

        statuts_etablissement_scolaire = individu(
            'statuts_etablissement_scolaire', period)
        eligibilite_statuts_etablissement_scolaire = (
            statuts_etablissement_scolaire == StatutsEtablissementScolaire.public) + (
            statuts_etablissement_scolaire == StatutsEtablissementScolaire.prive_sous_contrat)

        return occitanie_eligibilite_residence * eligibilite_scolarite * eligibilite_statuts_etablissement_scolaire
