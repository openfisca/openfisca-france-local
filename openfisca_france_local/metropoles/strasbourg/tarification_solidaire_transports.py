from openfisca_france.model.base import Variable, Individu, Menage, MONTH, YEAR, select


class eurometropole_strasbourg_tarification_solidaire_transport_eligibilite_geographique(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité géographique pour la tarification solidaire des transports de l'Eurométropole de Strasbourg"

    def formula(menage, period):
        return menage('menage_dans_epci_siren_246700488', period)


class eurometropole_strasbourg_tarification_solidaire_transport_quotient_familial_de_base(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Quotient familial pour la tarification solidaire des transports de l'Eurométropole de Strasbourg"

    def formula(individu, period):
        return individu.foyer_fiscal('rfr', period.n_2) / 12 / individu.foyer_fiscal('nbptr', period.n_2)


class eurometropole_strasbourg_tarification_solidaire_transport_quotient_familial(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Quotient familial pour la tarification solidaire des transports de l'Eurométropole de Strasbourg"


    def formula(individu, period):
        etudiant = individu('etudiant', period)
        qf_etudiant = individu('eurometropole_strasbourg_tarification_solidaire_transport_quotient_familial_etudiant', period)
        base = individu('eurometropole_strasbourg_tarification_solidaire_transport_quotient_familial_de_base', period)
        return select([etudiant], [qf_etudiant], default=base)


class eurometropole_strasbourg_tarification_solidaire_transport_quotient_familial_etudiant(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Équivalence du quotient familial d'étudiants pour la tarification solidaire des transports de l'Eurométropole de Strasbourg"


    def formula(individu, period):
        etudiant = individu('etudiant', period)
        boursier = individu('boursier', period)
        bourse_criteres_sociaux_echelon = individu('bourse_criteres_sociaux_echelon', period)
        return etudiant * select([boursier],[
            select(
            [
            5 <= bourse_criteres_sociaux_echelon,
            3 <= bourse_criteres_sociaux_echelon,
            1 <= bourse_criteres_sociaux_echelon,
            ],
            [
            355,
            560,
            765
            ],
            default=765)
          ],
          default=765)


class eurometropole_strasbourg_tarification_solidaire_transport_eligible_tarif_reduit(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Quotient familial pour la tarification solidaire des transports de l'Eurométropole de Strasbourg"

    def formula(individu, period):
        age = individu('age', period)
        taux_incapacite = individu('taux_incapacite', period)
        return (26 < age) + (65 <= age) + (0.80 <= taux_incapacite)


class eurometropole_strasbourg_tarification_solidaire_transport_montant(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Tarif de tarification solidaire des transports de l'Eurométropole de Strasbourg"
    reference = [
        "https://www.strasbourg.eu/tarification-solidaire-transports-en-commun"
        ]

    def formula(individu, period):
        geo = individu.menage('eurometropole_strasbourg_tarification_solidaire_transport_eligibilite_geographique', period)
        reduit = individu('eurometropole_strasbourg_tarification_solidaire_transport_eligible_tarif_reduit', period)
        qf = individu('eurometropole_strasbourg_tarification_solidaire_transport_quotient_familial', period)
        return geo * select(
            [qf <= 356, qf <= 560, qf < 765],
            [
                 5.8 + reduit * ( 3.4 -  5.8),
                13.4 + reduit * ( 7.3 - 13.4),
                25.7 + reduit * (13.6 - 25.7),
            ],
            default=select([reduit],[27.6], default=0)
            )
