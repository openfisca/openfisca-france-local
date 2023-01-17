from openfisca_france import CountryTaxBenefitSystem
from openfisca_core.taxbenefitsystems import TaxBenefitSystem


def test_dummy():
    tax_benefit_system: TaxBenefitSystem = CountryTaxBenefitSystem()
    assert tax_benefit_system.parameters.marche_travail.prime_pepa.parametre_inexistant
