from openfisca_france.model.base import Menage, MONTH, Variable

class montpellier_mutuelle_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage à la mutuelle communale de la métropole de Montpellier"
    reference = "https://encommun.montpellier.fr/articles/2024-12-19-lagence-de-la-mutuelle-communale-de-montpellier-est-ouverte"

    def formula(menage, period):
        return sum(menage('depcom', period) == code for code in [
            b'34172',  # Montpellier
            b'34077',  # Clapiers
            b'34090',  # Le Crès
            b'34179',  # Murviel-lès-Montpellier
            b'34256',  # Saint-Geniès-des-Mourgues
            b'34307'   # Sussargues
        ]) > 0
