from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france import CountryTaxBenefitSystem

qf = [410, 510, 620, 720, 820, 920, 1030, 1540, 2050, 2051, 2052]
#counts = [10, 10, 20, 20, 20, 20, 30, 40, 50]
counts2 = [4025, 2113, 1832, 1603, 962, 638, 566, 1990, 1157, 2090, 45]

# TEST_CASE = {
#   'individus': { 'individu'+str(q): { 'strasbourg_metropole_quotient_familial': { '2021-03': q } } for q in qf }
# }

TEST_CASE = {
  'individus': {
    'Gilles': {},
    'Jeanne': {
      'strasbourg_metropole_nombre_repas_cantine': {
        '2021-03': 15
      }
    },
    'Jacques': {},
    'Pauline': {
      'strasbourg_metropole_nombre_repas_cantine': {
        '2021-03': 20
      }
    }
  },
  'familles': {
    'Métro': {
      'parents': ['Gilles'],
      'enfants': ['Jeanne'],
      'strasbourg_metropole_quotient_familial': {
        '2021-03': 10000
      }
    },
    'Dupuis': {
       'parents': ['Jacques'],
       'enfants': ['Pauline'],
       'strasbourg_metropole_quotient_familial': {
        '2021-03': 827
      }
    }
  }
}

tax_benefit_system = CountryTaxBenefitSystem()
tax_benefit_system.load_extension('openfisca_france_local')
simulation_builder = SimulationBuilder()
simulation = simulation_builder.build_from_entities(tax_benefit_system, TEST_CASE)

tarif_cantine = simulation.calculate('strasbourg_metropole_tarification_cantine', '2021-03')

print('vecteur des tarifs')
print(tarif_cantine)

# sum_tranches = counts * tarif_cantine
# print('vecteur des recettes par tranche')
# print(sum_tranches)

# print('recettes totales')
# print(sum(sum_tranches))