from openfisca_france.model.base import Variable, Famille, MONTH, max_


class strasbourg_metropole_quotient_familial(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Quotient familial de l'eurometropole de strasbourg"

    def formula(famille, period):
        rfr = famille.demandeur.foyer_fiscal("rfr", period.n_2)
        nbptr = famille.demandeur.foyer_fiscal("nbptr", period.n_2)
        return rfr / 12 / nbptr


class strasbourg_metropole_tarification_solidaire_periscolaire(
    Variable
):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Tarification de l'accueil periscolaire de l'Eurométropole de Strasbourg"
    reference = [
        # tarifs pour 2021-2022 :
        "https://www.strasbourg.eu/documents/976405/1280877/0/0cc414e4-c6b7-1709-7e1e-46b088d28805",
        # tarifs 2202-2023
        "https://www.strasbourg.eu/documents/976405/1280877/0/c1917f09-97b2-2604-7d58-8b8cb5c0a849",
        # tarifs 2024-2025 :
        "https://www.strasbourg.eu/documents/976405/1280877/Tarifs-services-periscolaires-2024-2025.pdf/62fa6543-19ae-b69d-3313-13e881a6b866?version=1.0&t=1723127337051"
    ]

    def formula(famille, period, parameters):
        quotient_familial = famille("strasbourg_metropole_quotient_familial", period)
        tarif = parameters(
            period
        ).metropoles.strasbourg.periscolaire.accueil_soir_maternelle
        return tarif.calc(quotient_familial)
