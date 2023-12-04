import os
import pytest
from openfisca_france import FranceTaxBenefitSystem
from openfisca_france_local.aides_jeunes_reform import aides_jeunes_reform_dynamic


@pytest.mark.parametrize("bogus_benefit_folder", [
    'test_missing_condition_key',
    'test_missing_profile_key',
    'test_2_same_type_profils_with_same_type_condition',
    ])
def test_bogus_benefit_structure(bogus_benefit_folder):
    with pytest.raises(NotImplementedError):
        base_tbs = FranceTaxBenefitSystem()
        benefits_path = os.path.join('test_data/bogus_benefits/', bogus_benefit_folder)
        aides_jeunes_reform_dynamic(base_tbs, benefits_path)


def test_benefit_structures():
    base_tbs = FranceTaxBenefitSystem()

    # Path to benefits folder
    # To edit in local setup to path towards ALL benefits
    ok_path = os.getenv('OFFL_TEST_BENEFIT_PATH', "test_data/benefits")

    aides_jeunes_reform_dynamic(base_tbs, ok_path)
