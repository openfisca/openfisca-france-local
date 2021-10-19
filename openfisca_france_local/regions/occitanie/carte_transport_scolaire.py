from openfisca_france.model.base import Variable, Individu, MONTH, TypesActivite
from openfisca_france.model.prestations.education import StatutsEtablissementScolaire, TypesScolarite


class occitanie_carte_transport_scolaire_lio(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Eligibilité à la carte de transport scolaire liO"
    reference = "https://lio.laregion.fr/transport-scolaire"

    def formula(individu, period):
        occitanie_eligibilite_residence = individu.menage('occitanie_eligibilite_residence', period)

        scolarite = individu('scolarite', period)
        eligibilite_scolarite = (scolarite == TypesScolarite.maternelle) + \
                                (scolarite == TypesScolarite.primaire) + \
                                (scolarite == TypesScolarite.college) + \
                                (scolarite == TypesScolarite.lycee)

        statuts_etablissement_scolaire = individu('statuts_etablissement_scolaire', period)
        eligibilite_statuts_etablissement_scolaire = (statuts_etablissement_scolaire == StatutsEtablissementScolaire.public) + (statuts_etablissement_scolaire == StatutsEtablissementScolaire.prive_sous_contrat)

        return occitanie_eligibilite_residence * eligibilite_scolarite * eligibilite_statuts_etablissement_scolaire
