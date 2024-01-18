from os import chdir
from pathlib import Path

from openfisca_france import FranceTaxBenefitSystem
from openfisca_france_local import epci_test_factory


def test_epci_factory_path(tmp_path):
    '''
        Vérifie que le chemin utilisé dans la `epci_test_factory`
        est accessible quand le module est appellé depuis un autre projet
    '''
    # Change le dossier d'exécution pour simuler une utilisation dans un autre projet
    chdir(tmp_path)
    try:
        epci_test_factory.epci_reform(FranceTaxBenefitSystem())
    finally:
        # Remet le dossier d'exécution à son état d'origine
        chdir(Path(__file__).parent)
