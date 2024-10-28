from openfisca_france.model.base import Variable, Menage, MONTH

class eure_et_loir_eligibilite_aep(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité a l'Action Éducative de Promixité (AEP)"
    reference = [
        "https://eurelien.fr/wp-content/uploads/2023/01/l_aide_educative_de_proximite.pdf",
        "https://eurelien.fr/mon-quotidien/enfance-et-famille/#Laction-educative"
    ]

    def formula(menage, period):
        reside_eure_et_loir = menage('eure_et_loir_eligibilite_residence', period)
        enfants_a_charge = menage.members('enfant_a_charge', period.this_year)
        has_enfants_a_charge = menage.sum(enfants_a_charge) > 0

        return reside_eure_et_loir * has_enfants_a_charge
