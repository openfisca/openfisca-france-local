# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Menage, MONTH
from openfisca_core import reforms
from numpy.core.defchararray import startswith


def fsl_factory(prefix, dlabel, code_insee_departement):
    class NewFSLClass(Variable):
        value_type = bool
        entity = Menage
        definition_period = MONTH
        label = u"Ménage éligible à l'aide au maintien du FSL du département %s" % dlabel

        def formula(menage, period):
            return startswith(menage('depcom', period), code_insee_departement)

    NewFSLClass.__name__ = "%s_fonds_solidarite_logement_aide_maintien_eligibilite" % prefix
    return NewFSLClass


class fsl_reform(reforms.Reform):
    def apply(self):
        self.add_variable(fsl_factory('hautes_alpes', 'des Hautes Alpes', b'05'))
        self.add_variable(fsl_factory('alpes_maritimes', 'des Alpes Maritimes', b'06'))
        self.add_variable(fsl_factory('bouches_du_rhone', 'Des Bouches-du-Rhône', b'13'))
        self.add_variable(fsl_factory('calvados', 'du Calvados', b'14'))
        self.add_variable(fsl_factory('doubs', 'du Doubs', b'25'))
        self.add_variable(fsl_factory('finistere', 'du Finistère', b'29'))
        self.add_variable(fsl_factory('haute_garonne', 'de la Haute-Garonne', b'31'))
        self.add_variable(fsl_factory('gironde', 'de la Gironde', b'33'))
        self.add_variable(fsl_factory('herault', 'de l’Hérault', b'34'))
        self.add_variable(fsl_factory('ille_et_vilaine', 'd’Ille-et-Vilaine', b'35'))
        self.add_variable(fsl_factory('isere', 'd’Isère', b'38'))
        self.add_variable(fsl_factory('loire', 'de la Loire', b'42'))
        self.add_variable(fsl_factory('loire_atlantique', 'de la Loire Atlantique', b'44'))
        self.add_variable(fsl_factory('moselle', 'de la Moselle', b'57'))
        self.add_variable(fsl_factory('paris', 'de Paris', b'75'))
        self.add_variable(fsl_factory('seine_maritime', 'de Seine-Maritime', b'76'))
        self.add_variable(fsl_factory('seine_et_marne', 'de Seine-et-Marne', b'77'))
        self.add_variable(fsl_factory('var', 'du Var', b'83'))
        self.add_variable(fsl_factory('seine_saint_denis', 'de Seine-Saint-Denis', b'93'))
        self.add_variable(fsl_factory('var_de_marne', 'du Val-de-Marne', b'94'))
