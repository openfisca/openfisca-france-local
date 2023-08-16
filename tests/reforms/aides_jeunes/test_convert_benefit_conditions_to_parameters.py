from datetime import date
import yaml
import pytest
from openfisca_france import CountryTaxBenefitSystem

from openfisca_core.parameters import ParameterAtInstant, ParameterNode


from openfisca_france_local.convert_benefit_conditions_to_parameters\
    import convert_benefit_conditions_to_parameters


def generate_parameter_in_TBS(parameters: ParameterNode, benefit_path: str):
    benefit: dict = extract_benefit_file_content(benefit_path)

    new_parameter_node = convert_benefit_conditions_to_parameters(benefit)

    parameters.add_child(new_parameter_node.name, new_parameter_node)


@pytest.fixture
def parameters() -> ParameterNode:
    return CountryTaxBenefitSystem().parameters


@pytest.fixture
def test_folder() -> str:
    return 'test_data/benefits/'


@pytest.fixture
def test_condition_age_benefit_path() -> str:
    return 'test_data/benefits/test_condition_age.yaml'


def extract_benefit_file_content(benefit_path: str) -> dict:
    def _slug_from_Path(path: str):
        return path.split('/')[-1].replace('-', '_').split('.')[0]

    benefit: dict = yaml.safe_load(open(benefit_path))
    benefit['slug'] = _slug_from_Path(benefit_path)

    return benefit


def test_create_benefit_parameter_node(parameters: ParameterNode, test_condition_age_benefit_path: str):
    generate_parameter_in_TBS(parameters, test_condition_age_benefit_path)

    assert parameters.test_condition_age.conditions


def test_create_age_parameter_node(parameters: ParameterNode, test_condition_age_benefit_path: str):
    generate_parameter_in_TBS(parameters, test_condition_age_benefit_path)

    assert parameters.test_condition_age.conditions.age


def test_create_age_maximum_inclusif_parameter_node(parameters: ParameterNode, test_condition_age_benefit_path: str):
    generate_parameter_in_TBS(parameters, test_condition_age_benefit_path)

    assert parameters.test_condition_age.conditions.age.maximum_inclusif


def test_create_age_maximum_inclusif_parameter_with_value(parameters: ParameterNode, test_condition_age_benefit_path: str):
    generate_parameter_in_TBS(parameters, test_condition_age_benefit_path)

    assert parameters(str(date.today())).test_condition_age.conditions.age.maximum_inclusif == 25


def test_create_both_inclusive_age_parameter_node(parameters: ParameterNode, test_condition_age_benefit_path: str):
    generate_parameter_in_TBS(parameters, test_condition_age_benefit_path)

    benefit_parameter = parameters(str(date.today())).test_condition_age.conditions

    assert benefit_parameter.age.maximum_inclusif == 25 and \
        benefit_parameter.age.minimum_inclusif == 16


def test_create_age_maximum_exclusif_parameter_node(parameters: ParameterNode, test_folder: str):
    benefit_path: str = f'{test_folder}test_condition_age_maximum_exclusif.yaml'
    generate_parameter_in_TBS(parameters, benefit_path)

    benefit_parameter = parameters(str(date.today())).test_condition_age_maximum_exclusif.conditions.age.maximum_exclusif

    assert benefit_parameter == 25


def test_create_age_minimum_exclusif_parameter_node(parameters: ParameterNode, test_folder: str):
    benefit_path: str = f'{test_folder}test_condition_age_minimum_exclusif.yaml'
    generate_parameter_in_TBS(parameters, benefit_path)

    benefit_parameter = parameters(str(date.today())).test_condition_age_minimum_exclusif.conditions.age

    assert benefit_parameter.minimum_exclusif == 25


def test_create_quotient_familial_parameter(parameters: ParameterNode, test_folder: str):
    benefit_path: str = f'{test_folder}test_condition_quotient_familial.yaml'
    generate_parameter_in_TBS(parameters, benefit_path)

    at_instant: ParameterAtInstant = parameters("2023-01-01")
    parameter = at_instant.test_condition_quotient_familial

    assert parameter.conditions.quotient_familial.month.maximum_inclusif == 800


def test_create_region_parameter(parameters: ParameterNode, test_folder: str):
    benefit_path: str = f'{test_folder}test_condition_region_corse.yaml'
    generate_parameter_in_TBS(parameters, benefit_path)

    at_instant: ParameterAtInstant = parameters("2023-01-01")
    parameter = at_instant.test_condition_region_corse

    assert parameter.conditions.regions == ["94"]


def test_create_regime_securite_sociale_includes_parameter(parameters: ParameterNode, test_folder: str):
    benefit_path: str = f'{test_folder}test_condition_regime_securite_sociale_includes.yaml'
    generate_parameter_in_TBS(parameters, benefit_path)

    at_instant: ParameterAtInstant = parameters("2023-01-01")
    parameter = at_instant.test_condition_regime_securite_sociale_includes

    assert parameter.conditions.regime_securite_sociale.includes == ["regime_general"]


def test_create_regime_securite_sociale_excludes_parameter(parameters: ParameterNode, test_folder: str):
    benefit_path: str = f'{test_folder}test_condition_regime_securite_sociale_excludes.yaml'
    generate_parameter_in_TBS(parameters, benefit_path)

    at_instant: ParameterAtInstant = parameters("2023-01-01")
    parameter = at_instant.test_condition_regime_securite_sociale_excludes

    assert parameter.conditions.regime_securite_sociale.excludes == ["regime_agricole"]


def test_create_regime_securite_sociale_excludes_and_include_parameter():
    benefit: dict = {
        'label': "Aide au Brevet d'Aptitude aux Fonctions de Directeur (BAFD)",
        'conditions_generales': [{
            'type': 'regime_securite_sociale',
            'includes': ['regime_general'],
            'excludes': ['regime_agricole']
            }],

        'profils': [],
        'type': 'float',
        'montant': 286,
        'slug': 'test_condition_regime_securite_sociale_excludes_and_includes'
        }

    with pytest.raises(NotImplementedError):
        convert_benefit_conditions_to_parameters(benefit)


def test_create_formation_sanitaire_social_parameter(parameters: ParameterNode, test_folder: str):
    benefit_path: str = f'{test_folder}test_condition_formation_sanitaire_social_et_simples_profils.yaml'
    generate_parameter_in_TBS(parameters, benefit_path)

    at_instant: ParameterAtInstant = parameters("2023-01-01")
    parameter = at_instant.test_condition_formation_sanitaire_social_et_simples_profils

    assert parameter.conditions.formation_sanitaire_social


def test_create_empty_profil(parameters: ParameterNode, test_folder: str):
    benefit_path: str = f'{test_folder}test_profil_apprenti.yaml'
    generate_parameter_in_TBS(parameters, benefit_path)

    at_instant: ParameterAtInstant = parameters("2023-01-01")
    parameter = at_instant.test_profil_apprenti

    assert parameter.profils.apprenti


def test_create_profil_type_only(parameters: ParameterNode, test_folder: str):
    benefit_path: str = f'{test_folder}test_profil_etudiant.yaml'
    generate_parameter_in_TBS(parameters, benefit_path)

    at_instant: ParameterAtInstant = parameters("2023-01-01")
    parameter = at_instant.test_profil_etudiant

    assert parameter.profils.etudiant


def test_create_amount_106(parameters: ParameterNode, test_condition_age_benefit_path: str):
    generate_parameter_in_TBS(parameters, test_condition_age_benefit_path)

    at_instant: ParameterAtInstant = parameters("2023-01-01")
    assert at_instant.test_condition_age.montant == 106


def test_create_amount_1000(parameters: ParameterNode, test_folder: str):
    benefit_path: str = f'{test_folder}test_condition_beneficiaire_rsa.yaml'
    generate_parameter_in_TBS(parameters, benefit_path)

    at_instant: ParameterAtInstant = parameters("2023-01-01")
    assert at_instant.test_condition_beneficiaire_rsa.montant == 1000
