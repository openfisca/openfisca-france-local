import yaml
from openfisca_france import CountryTaxBenefitSystem
from openfisca_core.taxbenefitsystems import TaxBenefitSystem


def extract_benefit_file_content(benefit_path) -> dict:
    benefit: dict = yaml.safe_load(open(benefit_path))
    benefit['slug'] = benefit_path.split(
        '/')[-1].replace('-', '_').split('.')[0]
    return benefit


def test_dummy():
    tax_benefit_system: TaxBenefitSystem = CountryTaxBenefitSystem()
    assert tax_benefit_system.parameters.marche_travail.prime_pepa.plafond_salaire


def test_create_benefit_parameter_node():
    tax_benefit_system: TaxBenefitSystem = CountryTaxBenefitSystem()
    benefit_path = "benefits/caf_oise-aide-au-bafa-pour-une-session-de-formation-dapprofondissement-ou-de-qualification.yml"
    benefit = extract_benefit_file_content(benefit_path)

    new_parameter_node = create_benefit_parameters(benefit)
    tax_benefit_system.parameters.merge(new_parameter_node)

    assert tax_benefit_system.parameters.caf_oise_aide_au_bafa_pour_une_session_de_formation_dapprofondissement_ou_de_qualification
