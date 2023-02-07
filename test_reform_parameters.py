from datetime import date
import yaml
import pytest
from openfisca_france import CountryTaxBenefitSystem
from openfisca_france.model.base import (ParameterNode)

from condition_to_parameter import create_benefit_parameters
from openfisca_france_local.aides_jeunes_reform import aides_jeunes_reform_dynamic


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
                              "benefits/caf_oise-aide-au-bafa-pour-une-session-de-formation-dapprofondissement-ou-de-qualification.yaml")

    assert parameters.caf_oise_aide_au_bafa_pour_une_session_de_formation_dapprofondissement_ou_de_qualification.conditions


def test_create_age_parameter_node(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/caf_oise-aide-au-bafa-pour-une-session-de-formation-dapprofondissement-ou-de-qualification.yaml")

    assert parameters.caf_oise_aide_au_bafa_pour_une_session_de_formation_dapprofondissement_ou_de_qualification.conditions.age_maximum

def test_create_age_maximum_parameter_node(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/caf_oise-aide-au-bafa-pour-une-session-de-formation-dapprofondissement-ou-de-qualification.yaml")

    assert parameters.caf_oise_aide_au_bafa_pour_une_session_de_formation_dapprofondissement_ou_de_qualification.conditions.age_maximum


def test_create_age_maximum_parameter_with_value(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/caf_oise-aide-au-bafa-pour-une-session-de-formation-dapprofondissement-ou-de-qualification.yaml")

    assert parameters(str(date.today(
    ))).caf_oise_aide_au_bafa_pour_une_session_de_formation_dapprofondissement_ou_de_qualification.conditions.age_maximum == 16


def test_create_both_age_parameter_node(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/caf_pas_de_calais-aide-au-bafa-pour-une-session-de-formation-générale.yaml")

    benefit_parameter = parameters(str(date.today(
    ))).caf_pas_de_calais_aide_au_bafa_pour_une_session_de_formation_générale.conditions

    assert benefit_parameter.age_maximum == 25 and \
        benefit_parameter.age_minimum == 16


def test_create_age_strictement_inferieur_parameter_node(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/departement-val-d-oise-bourse-aux-apprentis.yaml")

    benefit_parameter = parameters(str(date.today(
    ))).departement_val_d_oise_bourse_aux_apprentis.conditions.age_strictement_inferieur

    assert benefit_parameter == 25


def test_create_age_strictement_superieur_parameter_node(parameters):

    benefit: dict = {
        "slug": "inf_parameter",
        "conditions_generales": [{'type': 'age', 'operator': '>', 'value': 25}]
    }

    new_parameter_node = create_benefit_parameters(benefit)
    parameters.add_child(
        new_parameter_node.name, new_parameter_node)

    assert parameters.inf_parameter.conditions.age_strictement_superieur


def test_create_age_value_parameter_node(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/departement-val-d-oise-bourse-aux-apprentis.yaml")

    at_instant = parameters("2023-01-01")
    parameter = at_instant.departement_val_d_oise_bourse_aux_apprentis

    assert parameter.conditions.age_strictement_inferieur == 25


def test_create_quotient_familial_parameter(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/caf_pas_de_calais-aide-au-bafa-pour-une-session-de-formation-générale.yaml")

    at_instant = parameters("2023-01-01")
    parameter = at_instant.caf_pas_de_calais_aide_au_bafa_pour_une_session_de_formation_générale

    assert parameter.conditions.quotient_familial.month.maximum == 1000


def test_create_region_parameter(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/hauts-de-france-carte-generation-apprentis-aide-transport.yaml")

    at_instant = parameters("2023-01-01")
    parameter = at_instant.hauts_de_france_carte_generation_apprentis_aide_transport

    assert parameter.conditions.regions == ["32"]


def test_create_regime_securite_sociale_parameter(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/caf_morbihan-aide-au-brevet-daptitude-aux-fonctions-de-directeur-bafd.yaml")

    at_instant = parameters("2023-01-01")
    parameter = at_instant.caf_morbihan_aide_au_brevet_daptitude_aux_fonctions_de_directeur_bafd

    assert parameter.conditions.regime_securite_sociale.includes == ["regime_general"]


def test_create_regime_securite_sociale_excludes_parameter(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/caf-val-de-marne-aide-bafa-approfondissement-qualification.yaml")

    at_instant = parameters("2023-01-01")
    parameter = at_instant.caf_val_de_marne_aide_bafa_approfondissement_qualification

    assert parameter.conditions.regime_securite_sociale.excludes == ["regime_agricole"]


def test_create_formation_sanitaire_social_parameter(parameters):
    generate_parameter_in_TBS(parameters,
                              "benefits/guadeloupe-bourse-sanitaire.yaml")

    at_instant = parameters("2023-01-01")
    parameter = at_instant.guadeloupe_bourse_sanitaire

    assert parameter.conditions.formation_sanitaire_social


def test_load_reforme_aides_jeunes():
    tbs = CountryTaxBenefitSystem()
    tbs_reformed = aides_jeunes_reform_dynamic(tbs)

    assert tbs_reformed.parameters.guadeloupe_bourse_sanitaire.conditions
