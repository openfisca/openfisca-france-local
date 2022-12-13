from openfisca_france.model.base import Variable, Individu, MONTH


class eure_et_loir_eligibilite_aep(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "En Eure-et-Loir, éligibilité a l'Action Éducative de Promixité (AEP)"
    reference = "https://www.eurelien.fr/sites/default/files/media/l_aide_educative_de_proximite.pdf"

    def formula(individu, period):
        reside_eure_et_loir = individu.menage('eure_et_loir_eligibilite_residence', period)
        enfants_a_charge = individu.menage.members('enfant_a_charge', period.this_year)
        has_enfants_a_charge = individu.menage.sum(enfants_a_charge) > 0

        return reside_eure_et_loir * has_enfants_a_charge