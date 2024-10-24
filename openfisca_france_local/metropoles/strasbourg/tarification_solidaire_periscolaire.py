from openfisca_france.model.base import Variable, Famille, MONTH, max_


class strasbourg_metropole_quotient_familial(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Quotient familial de l'eurometropole de strasbourg"

    # Note: pour le moment c'est le QF de la caf, mais à terme il poura evoluer pour se baser sur les revenus imposables
    def formula(famille, period):
        return (
            famille.demandeur.foyer_fiscal("rfr", period.n_2)
            / 12
            / famille.demandeur.foyer_fiscal("nbptr", period.n_2)
        )


class strasbourg_metropole_tarification_solidaire_periscolaire(
    Variable
):
    value_type = float
    entity = Famille
    definition_period = MONTH
    definition_period = MONTH
    label = "Tarification de l'acceuil periscolaire de l'Eurométropole de Strasbourg"
    reference = [
        # tarifs pour 2021-2022
        "https://www.strasbourg.eu/documents/976405/1280877/0/0cc414e4-c6b7-1709-7e1e-46b088d28805"
        # les tarifs 2202-2023 sont
        # https://www.strasbourg.eu/documents/976405/1280877/0/c1917f09-97b2-2604-7d58-8b8cb5c0a849
    ]

    def formula(famille, period, parameters):
        qf = famille("strasbourg_metropole_quotient_familial", period)
        tarif = parameters(
            period
        ).metropoles.strasbourg.periscolaire.acceuil_matin_soir_maternelle
        return tarif.calc(max_(0, qf), right=True)
