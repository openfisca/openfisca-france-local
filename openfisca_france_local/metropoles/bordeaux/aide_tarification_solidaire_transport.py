from openfisca_france.model.base import Variable, MONTH, Individu


class bordeaux_metropole_aide_tarification_solidaire_transport(Variable):
    entity = Individu
    definition_period = MONTH
    value_type = float
    label = "Éligibilité à l'aide tarification solidaire le la métropole de Bordeaux"
    reference = [
        'https://tarificationsolidaire.bordeaux-metropole.fr/Accueil.aspx']

    def formula(individu, period, parameters):
        rfr = individu.foyer_fiscal('rfr', period.this_year)
        nbptr = individu.foyer_fiscal('nbptr', period.this_year)
        qf = rfr / 12 / nbptr

        montant = 30
        return (qf <= 942) * montant
