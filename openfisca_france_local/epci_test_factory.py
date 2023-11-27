# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Menage, MONTH
from openfisca_core import reforms

from importlib.resources import as_file, files
import pandas as pd


def epci_test_factory(groups, code):
    group = groups.get_group(code)
    code_communes = group['insee'].values
    raison_sociale = group['raison_sociale'].values[0]

    class NewEPCITestClass(Variable):
        value_type = bool
        entity = Menage
        definition_period = MONTH
        label = u"Ménage dans une commune de l'EPCI %s" % raison_sociale

        def formula(menage, period):
            depcom = menage('depcom', period)
            return sum([depcom == code for code in code_communes])

    NewEPCITestClass.__name__ = "menage_dans_epci_siren_%i" % code
    return NewEPCITestClass


class epci_reform(reforms.Reform):
    def apply(self):
        with as_file(files('openfisca_france_local').joinpath('epcicom2020.xlsx')) as path:
            raw = pd.read_excel(path)
            raw.insee = raw.insee.astype('|S5')
            df = raw[['siren', 'insee', 'raison_sociale']].groupby('siren')

        for siren in df.groups:
            self.add_variable(epci_test_factory(df, siren))
