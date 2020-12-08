from openfisca_france.model.base import Variable, Individu, MONTH

class aide_menagere_fournie_caisse_retraite(Variable):
    value_type = bool
    label ="Prestations d’aide-ménagère servie par les caisses de retraite"
    entity = Individu
    definition_period = MONTH
    default_value = False