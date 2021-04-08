from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france import CountryTaxBenefitSystem

qf = [410, 510, 620, 720, 820, 920, 1030, 1540, 2050, 2051, 2052]
counts = [4025, 2113, 1832, 1603, 962, 638, 566, 1990, 1157, 2090, 45] 

TEST_CASE = {
  'individus': { 'enf_'+str(q): {} for q in qf },
  'familles': {
    'famille_'+str(q): {
      'enfants': ['enf_'+str(q)],
      'strasbourg_metropole_quotient_familial': { '2021-03': q }
    } for q in qf
  },
}

from pprint import pprint
pprint(TEST_CASE)

tax_benefit_system = CountryTaxBenefitSystem()
tax_benefit_system.load_extension('openfisca_france_local')
simulation_builder = SimulationBuilder()
simulation = simulation_builder.build_from_entities(tax_benefit_system, TEST_CASE)

tarif_cantine = simulation.calculate('strasbourg_metropole_tarification_cantine', '2021-03')

print('vecteur des tarifs')
print(tarif_cantine)

sum_tranches = counts * tarif_cantine * 200 # Pour 200 repas par an
print('vecteur des recettes par tranche')
print(sum_tranches)

print('recettes totales')
print(sum(sum_tranches))
