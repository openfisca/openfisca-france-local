import yaml
import pytest
from openfisca_france import CountryTaxBenefitSystem
from openfisca_france.model.base import (ParameterNode)

from condition_to_parameter import create_benefit_parameters


@pytest.fixture
def tax_benefit_system() -> ParameterNode:
    return CountryTaxBenefitSystem().parameters


def extract_benefit_file_content(benefit_path) -> dict:
    benefit: dict = yaml.safe_load(open(benefit_path))
    benefit['slug'] = benefit_path.split(
        '/')[-1].replace('-', '_').split('.')[0]
    return benefit


def test_create_benefit_parameter_node(tax_benefit_system):
    benefit_path = "benefits/caf_oise-aide-au-bafa-pour-une-session-de-formation-dapprofondissement-ou-de-qualification.yml"
    benefit = extract_benefit_file_content(benefit_path)

    new_parameter_node = create_benefit_parameters(benefit)
    tax_benefit_system.parameters.add_child(
        new_parameter_node.name, new_parameter_node)

    assert tax_benefit_system.parameters.caf_oise_aide_au_bafa_pour_une_session_de_formation_dapprofondissement_ou_de_qualification


def test_create_age_parameter_node(tax_benefit_system):
    benefit_path = "benefits/caf_oise-aide-au-bafa-pour-une-session-de-formation-dapprofondissement-ou-de-qualification.yml"
    benefit = extract_benefit_file_content(benefit_path)

    new_parameter_node = create_benefit_parameters(benefit)
    tax_benefit_system.parameters.add_child(
        new_parameter_node.name, new_parameter_node)

    assert tax_benefit_system.parameters.caf_oise_aide_au_bafa_pour_une_session_de_formation_dapprofondissement_ou_de_qualification.age


def test_create_age_maximum_parameter_node(tax_benefit_system):
    benefit_path = "benefits/caf_oise-aide-au-bafa-pour-une-session-de-formation-dapprofondissement-ou-de-qualification.yml"
    benefit = extract_benefit_file_content(benefit_path)

    new_parameter_node = create_benefit_parameters(benefit)
    tax_benefit_system.parameters.add_child(
        new_parameter_node.name, new_parameter_node)

    assert tax_benefit_system.parameters.caf_oise_aide_au_bafa_pour_une_session_de_formation_dapprofondissement_ou_de_qualification.age.maximum


def test_create_age_strictement_inferieur_parameter_node(tax_benefit_system):
    benefit_path = "benefits/departement-val-d-oise-bourse-aux-apprentis.yml"
    benefit = extract_benefit_file_content(benefit_path)

    new_parameter_node = create_benefit_parameters(benefit)
    tax_benefit_system.parameters.add_child(
        new_parameter_node.name, new_parameter_node)

    assert tax_benefit_system.parameters.departement_val_d_oise_bourse_aux_apprentis.age.strictement_inferieur


def test_create_age_strictement_superieur_parameter_node(tax_benefit_system):

    benefit: dict = {
        "slug": "inf_parameter",
        "conditions_generales": [{'type': 'age', 'operator': '>', 'value': 25}]
    }

    new_parameter_node = create_benefit_parameters(benefit)
    tax_benefit_system.parameters.add_child(
        new_parameter_node.name, new_parameter_node)

    assert tax_benefit_system.parameters.inf_parameter.age.strictement_superieur


def test_create_age_value_parameter_node(tax_benefit_system):
    benefit_path = "benefits/departement-val-d-oise-bourse-aux-apprentis.yml"
    benefit = extract_benefit_file_content(benefit_path)

    new_parameter_node = create_benefit_parameters(benefit)
    tax_benefit_system.parameters.add_child(
        new_parameter_node.name, new_parameter_node)

    at_instant = tax_benefit_system.parameters("2023-01-01")
    parameter = at_instant.departement_val_d_oise_bourse_aux_apprentis

    assert parameter.age.strictement_inferieur == 25
