 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Famille, Individu, MONTH
from openfisca_france.model.prestations.education import TypesScolarite

from numpy.core.defchararray import startswith


class seine_saint_denis_cheque_reussite(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

    def formula(famille, period):
        return famille.sum(famille.members('seine_saint_denis_cheque_reussite_montant', period))


class seine_saint_denis_cheque_reussite_montant(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        return 200 * individu('seine_saint_denis_cheque_reussite_eligibilite', period)


class seine_saint_denis_cheque_reussite_6eme(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        return individu('scolarite', period) == TypesScolarite.college


class seine_saint_denis_cheque_reussite_eligibilite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        resid = individu.menage('seine_saint_denis_eligibilite_residence', period)
        en6eme = individu('seine_saint_denis_cheque_reussite_6eme', period)
        
        return resid * en6eme
