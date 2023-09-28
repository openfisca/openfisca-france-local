from openfisca_france.model.base import (
    Variable,
    Individu,
    Famille,
    Menage,
    MONTH,
    YEAR,
    select,
)
import numpy as np


class eurometropole_strasbourg_tarification_solidaire_transport_eligibilite_geographique(
    Variable
):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité géographique pour la tarification solidaire des transports de l'Eurométropole de Strasbourg"

    def formula(menage, period):
        return menage("menage_dans_epci_siren_246700488", period)


class emeraude(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH


class eurometropole_strasbourg_tarification_solidaire_transport_annuel(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH


class eurometropole_strasbourg_tarification_solidaire_transport_quotient_familial(
    Variable
):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Quotient familial pour la tarification solidaire des transports de l'Eurométropole de Strasbourg"

    def formula(individu, period):
        etudiant = individu("etudiant", period)
        qf_etudiant = individu(
            "eurometropole_strasbourg_tarification_solidaire_transport_quotient_familial_etudiant",
            period,
        )
        base = individu.famille("strasbourg_metropole_quotient_familial", period)
        return select([etudiant], [qf_etudiant], default=base)


class eurometropole_strasbourg_tarification_solidaire_transport_quotient_familial_etudiant(
    Variable
):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Équivalence du quotient familial d'étudiants pour la tarification solidaire des transports de l'Eurométropole de Strasbourg"

    def formula(individu, period, parameters):
        etudiant = individu("etudiant", period)
        boursier = individu("boursier", period)
        bourse_criteres_sociaux_echelon = individu(
            "bourse_criteres_sociaux_echelon", period
        )

        P = parameters(period).metropoles.strasbourg.tarification_solidaire
        correspondance_echelon = P.correspondance_echelon_qf
        return etudiant * (
            boursier * correspondance_echelon.calc(bourse_criteres_sociaux_echelon)
            + (1 - boursier) * 765
        )


class eurometropole_strasbourg_tarification_solidaire_transport_eligible_tarif_reduit_age(
    Variable
):
    value_type = bool
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        age = individu("age", period)
        return (age < 26) + (65 <= age)


class eurometropole_strasbourg_tarification_solidaire_transport_eligible_tarif_reduit_handicap(
    Variable
):
    value_type = bool
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        taux_incapacite = individu("taux_incapacite", period)
        return 0.80 <= taux_incapacite


class eurometropole_strasbourg_tarification_solidaire_transport_montant(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Tarif de tarification solidaire des transports de l'Eurométropole de Strasbourg"
    reference = [
        "https://www.strasbourg.eu/tarification-solidaire-transports-en-commun"
    ]

    def formula(individu, period, parameters):
        geo = individu.menage(
            "eurometropole_strasbourg_tarification_solidaire_transport_eligibilite_geographique",
            period,
        )
        reduit = individu(
            "eurometropole_strasbourg_tarification_solidaire_transport_eligible_tarif_reduit",
            period,
        )
        qf = individu(
            "eurometropole_strasbourg_tarification_solidaire_transport_quotient_familial",
            period,
        )
        bareme = parameters(period).metropoles.strasbourg.tarification_solidaire.bareme
        bareme_reduit = parameters(
            period
        ).metropoles.strasbourg.tarification_solidaire.bareme_reduit

        montant = reduit * bareme_reduit.calc(qf) + (1 - reduit) * bareme.calc(qf)
        return geo * montant


class eurometropole_strasbourg_tarification_transport(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Tarif de tarification solidaire des transports de l'Eurométropole de Strasbourg"
    reference = [
        "https://www.strasbourg.eu/tarification-solidaire-transports-en-commun"
    ]

    def formula(individu, period, parameters):
        emeraude = individu("emeraude", period)
        geo = individu.menage(
            "eurometropole_strasbourg_tarification_solidaire_transport_eligibilite_geographique",
            period,
        )
        reduit_age = individu(
            "eurometropole_strasbourg_tarification_solidaire_transport_eligible_tarif_reduit_age",
            period,
        )
        reduit_handicap = individu(
            "eurometropole_strasbourg_tarification_solidaire_transport_eligible_tarif_reduit_handicap",
            period,
        )
        qf = individu(
            "eurometropole_strasbourg_tarification_solidaire_transport_quotient_familial",
            period,
        )

        P = parameters(period).metropoles.strasbourg.tarification_solidaire

        bareme = P.bareme
        bareme_reduit_age = P.bareme_reduit_age
        bareme_reduit_handicap = P.bareme_reduit_handicap
        bareme_emeraude = P.bareme_emeraude

        bareme_annuel = P.annuel.bareme
        bareme_annuel_reduit_age = P.annuel.bareme_reduit_age
        bareme_annuel_reduit_handicap = P.annuel.bareme_reduit_handicap

        montant_mensuel = np.select(
            [emeraude, reduit_age, reduit_handicap],
            [
                bareme_emeraude.calc(qf),
                bareme_reduit_age.calc(qf),
                bareme_reduit_handicap.calc(qf),
            ],
            default=bareme.calc(qf),
        )
        montant_annuel = np.select(
            [reduit_age, reduit_handicap],
            [bareme_annuel_reduit_age.calc(qf), bareme_annuel_reduit_handicap.calc(qf)],
            default=bareme_annuel.calc(qf),
        )

        annuel = individu(
            "eurometropole_strasbourg_tarification_solidaire_transport_annuel", period
        )

        montant = np.where(annuel, montant_annuel, montant_mensuel)
        return geo * montant
