import yaml
import pytest
from openfisca_france import CountryTaxBenefitSystem
from openfisca_france.model.base import (ParameterNode)

from condition_to_parameter import create_benefit_parameters


def generate_parameter_in_TBS(parameters, benefit_path):
    benefit = extract_benefit_file_content(benefit_path)

    new_parameter_node = create_benefit_parameters(benefit)
    parameters.add_child(
        new_parameter_node.name, new_parameter_node)


@pytest.fixture
def parameters() -> ParameterNode:
    return CountryTaxBenefitSystem().parameters


def extract_benefit_file_content(benefit_path) -> dict:
    benefit: dict = yaml.safe_load(open(benefit_path))
    benefit['slug'] = benefit_path.split(
        '/')[-1].replace('-', '_').split('.')[0]
    return benefit


def test_create_benefit_parameter_node(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/caf_oise-aide-au-bafa-pour-une-session-de-formation-dapprofondissement-ou-de-qualification.yml")

    assert parameters.caf_oise_aide_au_bafa_pour_une_session_de_formation_dapprofondissement_ou_de_qualification


def test_create_age_parameter_node(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/caf_oise-aide-au-bafa-pour-une-session-de-formation-dapprofondissement-ou-de-qualification.yml")

    assert parameters.caf_oise_aide_au_bafa_pour_une_session_de_formation_dapprofondissement_ou_de_qualification.age


def test_create_age_maximum_parameter_node(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/caf_oise-aide-au-bafa-pour-une-session-de-formation-dapprofondissement-ou-de-qualification.yml")

    assert parameters.caf_oise_aide_au_bafa_pour_une_session_de_formation_dapprofondissement_ou_de_qualification.age.maximum


def test_create_age_strictement_inferieur_parameter_node(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/departement-val-d-oise-bourse-aux-apprentis.yml")

    assert parameters.departement_val_d_oise_bourse_aux_apprentis.age.strictement_inferieur


def test_create_age_strictement_superieur_parameter_node(parameters):

    benefit: dict = {
        "slug": "inf_parameter",
        "conditions_generales": [{'type': 'age', 'operator': '>', 'value': 25}]
    }

    new_parameter_node = create_benefit_parameters(benefit)
    parameters.add_child(
        new_parameter_node.name, new_parameter_node)

    assert parameters.inf_parameter.age.strictement_superieur


def test_create_age_value_parameter_node(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/departement-val-d-oise-bourse-aux-apprentis.yml")

    at_instant = parameters("2023-01-01")
    parameter = at_instant.departement_val_d_oise_bourse_aux_apprentis

    assert parameter.age.strictement_inferieur == 25


def test_create_quotient_familial_parameter(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/caf_pas_de_calais-aide-au-bafa-pour-une-session-de-formation-générale.yml")

    at_instant = parameters("2023-01-01")
    parameter = at_instant.caf_pas_de_calais_aide_au_bafa_pour_une_session_de_formation_générale

    assert parameter.quotient_familial.month.maximum == 1000


def test_create_region_parameter(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/hauts-de-france-carte-generation-apprentis-aide-transport.yml")

    at_instant = parameters("2023-01-01")
    parameter = at_instant.hauts_de_france_carte_generation_apprentis_aide_transport

    assert parameter.regions == ["32"]


def test_create_regime_securite_sociale_parameter(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/caf_morbihan-aide-au-brevet-daptitude-aux-fonctions-de-directeur-bafd.yml")

    at_instant = parameters("2023-01-01")
    parameter = at_instant.caf_morbihan_aide_au_brevet_daptitude_aux_fonctions_de_directeur_bafd

    assert parameter.regime_securite_sociale == ["regime_general"]
