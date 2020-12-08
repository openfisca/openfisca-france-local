from openfisca_france.model.base import Variable, Individu, MONTH

class aide_menagere_fournie_caisse_retraite(Variable):
    value_type = bool
    label ="Prestations d’aide-ménagère servie par les caisses de retraite"
    entity = Individu
    definition_period = MONTH
    default_value = False

class actp(Variable):
    value_type = bool
    label ="Bénéficiaire de l'Allocation compensatrice pour tierce personne"
    entity = Individu
    definition_period = MONTH
    default_value = False

class mtp(Variable):
    value_type = bool
    label ="Bénéficiaire de la Majoration Tierce Personne"
    entity = Individu
    definition_period = MONTH
    default_value = False

class refugie(Variable):
    value_type = bool
    label = "La personne est réfugié"
    entity = Individu
    definition_period = MONTH
    default_value = False

class apatride(Variable):
    value_type = bool
    label = "La personne est apatride"
    entity = Individu
    definition_period = MONTH
    default_value = False
