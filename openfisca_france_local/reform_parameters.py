from pathlib import Path
import yaml
from openfisca_core import reforms
from openfisca_france.model.base import (ParameterNode, Parameter)
from openfisca_france.model.base import *

from condition_to_parameter import create_benefit_parameters


class aides_jeunes_parameter_reform(reforms.Reform):
    root = '.'
    path = 'benefits/'
    current_path = f'{root}/{path}'

    def extract_benefit_file_content(self, benefit_path):
        benefit: dict = yaml.safe_load(open(benefit_path))
        benefit['slug'] = benefit_path.split(
            '/')[-1].replace('-', '_').split('.')[0]
        return benefit

    def extract_benefits_paths(self, benefits_folder: str) -> "list[str]":
        def isYAMLfile(path: str): return str(path).endswith(
            '.yml') or str(path).endswith('.yaml')
        liste_fichiers = [
            str(benefit) for benefit in Path(benefits_folder).iterdir() if isYAMLfile(benefit)]
        return liste_fichiers

    def apply(self):
        try:
            benefit_files_paths = self.extract_benefits_paths(
                self.current_path)
            benefit = self.extract_benefit_file_content(benefit_files_paths[0])
            parameter = create_benefit_parameters(benefit)
            print(parameter)
            self.parameters.merge(parameter)
            # for path in benefit_files_paths:
            # benefit: dict = self.extract_benefit_file_content(path)

        except KeyError as e:
            raise KeyError(f"field {e} missing in file: a")
            # raise KeyError(f"field {e} missing in file: {path}")

# class aides_jeunes_test_parameter(reforms.Reform):
#     class test_variable_w2(Variable):
#         value_type = bool
#         entity = Individu
#         definition_period = MONTH
#         label = u"fwefwef"

#         def formula(individu, period, parameters):

#             print(f'{(type(parameters(period).easy))}')
#             print(f'{type(individu("age", period.first_month))}')

#             age = individu("age", period.first_month)
#             return sum([[parameters(period).easy] * age])

#     simple_parameter = ParameterNode('', data={
#         "easy": {"1900-12-12": {
#             "value": 24}, }
#     })

#     def apply(self):
#         self.parameters.merge(self.simple_parameter)
#         self.add_variable(self.test_variable_w2)
