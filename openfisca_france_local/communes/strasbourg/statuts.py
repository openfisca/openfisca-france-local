from openfisca_france.model.base import *

class evasion(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH


class cada(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH


class habitant_ems(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH


class agent_ems(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH


class CCSTarif(Enum):
    # __order__ = ''
    TP = "TP"
    RA = "RA"
    RB = "RB"


class strasbourg_centre_choregraphique_tarif(Variable):
    value_type = Enum
    default_value = CCSTarif.TP
    possible_values = CCSTarif
    entity = Famille
    definition_period = MONTH
