from openfisca_france.model.base import Variable, MONTH, Famille


class bordeaux_metropole_aide_tarification_solidaire_transport(Variable):
    entity = Famille
    definition_period = MONTH
    value_type = float
    label = "Éligibilité à l'aide tarification solidaire le la métropole de Bordeaux"
    reference = [
        'https://tarificationsolidaire.bordeaux-metropole.fr/Accueil.aspx']

    def formula(individu, period, parameters):
        return False
