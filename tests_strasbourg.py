from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france import CountryTaxBenefitSystem

qf = [410, 510, 620, 720, 820, 920, 1030, 1540, 2050, 2051, 2052]
counts = [4025, 2113, 1832, 1603, 962, 638, 566, 1990, 1157, 2090, 45] 

# le cas de test décrit 150 repas pour une année pour les familles 

TEST_CASE = {
  'individus': { 'enf_'+str(q): { 'strasbourg_metropole_nombre_repas_cantine': { '2021-03': 150 } } for q in qf },
  'familles': {
    'famille_'+str(q): {
      'enfants': ['enf_'+str(q)],
      'strasbourg_metropole_quotient_familial': { '2021-03': q }
    } for q in qf
  },
}

TEST_CASE = {
  'individus': { 'enf_'+str(499): { 'strasbourg_metropole_nombre_repas_cantine': { '2021-03': 150 } } },
  'familles': {
    'famille_'+str(499): {
      'enfants': ['enf_'+str(499)],
      'strasbourg_metropole_quotient_familial': { '2021-03': 499 }
    } 
  },
}

TEST_CASE = {
  'individus': { 'enf_'+str(650): { 'strasbourg_metropole_nombre_repas_cantine': { '2021-03': 170 } } },
  'familles': {
    'famille_'+str(650): {
      'enfants': ['enf_'+str(650)],
      'strasbourg_metropole_quotient_familial': { '2021-03': 650 }
    } 
  },
}

from pprint import pprint
pprint(TEST_CASE)

tax_benefit_system = CountryTaxBenefitSystem()
tax_benefit_system.load_extension('openfisca_france_local')
simulation_builder = SimulationBuilder()
simulation = simulation_builder.build_from_entities(tax_benefit_system, TEST_CASE)

tarif_cantine = simulation.calculate('strasbourg_metropole_tarification_cantine', '2021-03') 
# ce que va payer sur la durée la famille par tranche de QF 
cout_cantine = simulation.calculate( 'strasbourg_metropole_cout_cantine', '2021-03') 
# ce que la collectivité va recevoir sur la durée par tranche de QF 

print('vecteur des tarifs')
print(tarif_cantine)
print('vecteur des couts')
print(cout_cantine)

sum_tranches = counts * tarif_cantine * 170 # Pour 150 repas par an
print('vecteur des recettes par tranche')
print(sum_tranches)

print('recettes totales')
print(sum(sum_tranches))

sum_tranches = counts * cout_cantine # pour 150 repas par an 
print('vecteur des recettes par tranche')
print(sum_tranches)

print('recettes totales')
print(sum(sum_tranches))