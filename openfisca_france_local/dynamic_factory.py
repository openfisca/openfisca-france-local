# -*- coding: utf-8 -*-
from openfisca_core import reforms
import ast
import tempfile
import types
import importlib.machinery
import os
import glob
import pathlib
import yaml


class dynamic_reform(reforms.Reform):
    def apply(self):
        filenames = glob.glob(os.path.join(pathlib.Path(__file__).parent.absolute(), '..', 'tests', 'dynamic', "**.yaml"))
        for filename in filenames:
            with open(filename) as variable_file:
                variable_metadata = yaml.safe_load(variable_file)

                with tempfile.NamedTemporaryFile('w') as f:
                    file_root, _ = os.path.splitext(filename)
                    name = os.path.basename(file_root)
                    label = variable_metadata['name']
                    formula = variable_metadata['formula']

                    expr = ast.parse(formula)
                    assert len(expr.body) == 1
                    assert type(expr.body[0]) == ast.Expr

                    person_deps = []
                    group_deps = []
                    for node in ast.walk(expr):
                        if type(node) != ast.Name:
                            continue
                        if node.id == 'P':
                            continue
                        if node.id not in self.variables:
                            raise ValueError("'{}'' variable does not exist.".format(node.id))
                        variable = self.variables[node.id]

                        if variable.entity.is_person:
                            person_deps.append(node.id)
                        else:
                            group_deps.append((variable.entity.key, node.id))

                    person_variables = "\n".join(["{}{} = individu('{}', period)".format("        ", d, d) for d in person_deps])
                    group_variables = "\n".join(["{}{} = individu.{}('{}', period)".format("        ", name, group, name) for (group, name) in group_deps])
                    f.write("""
from openfisca_france.model.base import Variable, Individu, MONTH

class {}(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        P = parameters(period)
{} # variables associées aux individus
{} # variables associées aux groupes (familles, etc.)

        return {}
""".format(name, person_variables, group_variables, formula))
                    f.seek(0)
                    loader = importlib.machinery.SourceFileLoader('dynamicmodule', f.name)
                    mod = types.ModuleType(loader.name)
                    loader.exec_module(mod)
                    self.add_variable(getattr(mod, name))
