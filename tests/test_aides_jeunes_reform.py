import os
import pytest
from openfisca_france import FranceTaxBenefitSystem
from openfisca_france.scenarios import init_single_entity
from openfisca_france_local.aides_jeunes_reform import aides_jeunes_reform_dynamic


@pytest.mark.parametrize("bogus_benefit_folder", [
    'bogus_benefits/test_missing_condition_key',
    'bogus_benefits/test_missing_profile_key',
])
def test_bogus_benefit_structure(bogus_benefit_folder):
    with pytest.raises(KeyError):
        base_tbs = FranceTaxBenefitSystem()
        aides_jeunes_reform_dynamic(base_tbs, bogus_benefit_folder)


def test_benefit_structures():
    base_tbs = FranceTaxBenefitSystem()

    # Path to benefits folder
    # To edit in local setup to path towards ALL benefits
    ok_path = "benefits"

    aides_jeunes_reform_dynamic(base_tbs, ok_path)
