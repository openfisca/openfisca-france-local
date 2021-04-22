from openfisca_france.model.base import *

class nombre_individus_inscrits(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

class nombre_familles(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

class nombre_foyers_fiscaux(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = MONTH

class nombre_menages(Variable):
    value_type = float
    entity = Menage
    definition_period = MONTH
