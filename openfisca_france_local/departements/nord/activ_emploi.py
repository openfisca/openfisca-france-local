from openfisca_france.model.base import Variable, Menage, Individu, MONTH
from numpy.core.defchararray import startswith


class nord_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs du département du Nord"

    def formula(menage, period):
        return startswith(menage('depcom', period), b'59')


class nord_activ_emploi_eligibilite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité au dispositif Activ'Emploi du département du Nord"

    def formula(individu, period):
        eligible_residence = individu.menage('nord_eligibilite_residence', period)
        recoit_rsa = individu.famille('rsa', period) > 0
        return eligible_residence * recoit_rsa


class nord_activ_emploi_maximum(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    reference = "https://lenord.fr/jcms/prd1_608417/activ-emploi"
    label = "Montant maximum de l'aide financière Activ'Emploi du département du Nord"

    def formula(individu, period):
        eligible = individu('nord_activ_emploi_eligibilite', period)
        return 150 * eligible
