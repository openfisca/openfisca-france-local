 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Famille, Individu, MONTH
from openfisca_france.model.prestations.education import TypesScolarite

from numpy.core.defchararray import startswith


class seine_saint_denis_cheque_reussite(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Montant pour une famille des chèque réussite du département de la Seine-Saint-Denis"

    def formula(famille, period):
        return famille.sum(famille.members('seine_saint_denis_cheque_reussite_montant', period))


class seine_saint_denis_cheque_reussite_montant(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant par enfant du chèque réussite du département de la Seine-Saint-Denis"
    reference = [
        "https://seinesaintdenis.fr/enfance-education-jeunesse/colleges/article/un-cheque-reussite-de-200-eur-pour-les-sixiemes"
        ]

    def formula(individu, period):
        return 200 * individu('seine_saint_denis_cheque_reussite_eligibilite', period)


class seine_saint_denis_cheque_reussite_eligibilite_classe(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Critère de scolarisation d'enfant pour l'éligibilité au chèque réussite du département de la Seine-Saint-Denis"

    def formula(individu, period):
        return individu('scolarite', period) == TypesScolarite.college


class seine_saint_denis_cheque_reussite_eligibilite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité d'un enfant au chèque réussite du département de la Seine-Saint-Denis"

    def formula(individu, period):
        resid = individu.menage('seine_saint_denis_eligibilite_residence', period)
        classe_ok = individu('seine_saint_denis_cheque_reussite_eligibilite_classe', period)
        
        return resid * classe_ok
