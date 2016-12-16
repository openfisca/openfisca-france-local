# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select, where,logical_or as or_)
 
from openfisca_france.model.base import *  # noqa analysis:ignore

class rennes_metropole_transport(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Calcul tarification solidaire"

    def function(self, simulation, period):
        period = period.this_month
        nombre_enfants = simulation.calculate('af_nbenf', period)
        # montant_par_enfant = simulation.legislation_at(period.start).rennesmetropole.mon_aide.montant
        

        ressources_a_inclure =[

            'salaire_net',
            'indemnites_journalieres',
            'allocation_aide_retour_emploi',
            'ass',
            'rsa',
           # 'ppa',
            'pensions_invalidite',
            'revenus_stage_formation_pro',
            'af',
            'cf',
            'asf',
            'paje_base',
            'paje_clca',
            'paje_prepare',
            #'ajpp',
            'aide_logement',
            #'alf',
            #'als',
            'aah',
            'retraite_nette',
            'retraite_combattant',
            'aspa',
            'pensions_alimentaires_percues',
            'revenus_locatifs',
            'revenus_capital',
            


        ]
        
        #pensions_alimentaires_versees 
       
        #renvenus BIC ou B
        def revenus_tns():
            revenus_auto_entrepreneur = simulation.calculate_add('tns_auto_entrepreneur_benefice', period.last_3_months)
           

            # Les revenus TNS hors AE sont estimés en se basant sur le revenu N-1
            tns_micro_entreprise_benefice = simulation.calculate('tns_micro_entreprise_benefice', period.last_year) * (3 / 12)
            tns_benefice_exploitant_agricole = simulation.calculate('tns_benefice_exploitant_agricole', period.last_year) * (3 / 12)
            tns_autres_revenus = simulation.calculate('tns_autres_revenus', period.last_year) * (3 / 12)
            return revenus_auto_entrepreneur + tns_micro_entreprise_benefice + tns_benefice_exploitant_agricole + tns_autres_revenus
 

        ressources=sum([simulation.calculate_add(ressource,period.start.period('year').offset(-1))/12 for ressource in ressources_a_inclure]) - simulation.calculate('pensions_alimentaires_versees_individu', period.last_3_months) + revenus_tns()

        #ajout de la ppa
        ressources=ressources+(simulation.calculate('ppa',period.last_year)) * (3 / 12)
         
        #print (simulation.calculate_add('rsa',period.last_year))
       # ressources = ressources / 12
      #  print(simulation.calculate_add('aide_logement',period.last_year))
      #  print(simulation.calculate_add('salaire_net',period.last_year))
        #recherche si en couple
        famille_en_couple =simulation.compute('en_couple', period)
        #transformation valeur en couple sur l'entity Famille
        individu_en_couple = self.cast_from_entity_to_roles(famille_en_couple)
       
        seuil1= simulation.legislation_at(period.start).rennesmetropole.tarification_solidaire.seuil.seuil1      
        seuil2 = simulation.legislation_at(period.start).rennesmetropole.tarification_solidaire.seuil.seuil2
        seuil3 = simulation.legislation_at(period.start).rennesmetropole.tarification_solidaire.seuil.seuil3

        taux1= simulation.legislation_at(period.start).rennesmetropole.tarification_solidaire.taux_reduction.taux1      
        taux2 = simulation.legislation_at(period.start).rennesmetropole.tarification_solidaire.taux_reduction.taux2
        taux3 = simulation.legislation_at(period.start).rennesmetropole.tarification_solidaire.taux_reduction.taux3

		# determine si une personne seule a des enfants qui est considéré de fait comme un couple
        individu_en_couple = or_(individu_en_couple,nombre_enfants>=1)

        #salaire =  simulation.compute('salaire_net', period)
       # salaire_cumul=self.sum_by_entity(salaire, entity = 'famille')

        seuil_evolutif=(1+individu_en_couple*(0.5+nombre_enfants*0.3))
        
        

        result_non_etudiant = select([ressources <= seuil1*seuil_evolutif,ressources <= seuil2*seuil_evolutif, ressources <= seuil3*seuil_evolutif], [taux1,taux2,taux3])
       
        # import ipdb
        # ipdb.set_trace()
        etudiant = simulation.calculate('etudiant')
       
        #result_etudiant = simulation.calculate('rennes_metropole_transport_etudiant')
        
        # Récupération de l'échelon de bourse
        echelon = simulation.calculate('echelon_bourse',period)
        #echelon = 4
        #print(echelon)
        result_etudiant = select([echelon >= 5,echelon >= 3, echelon >= 2], [taux1,taux2,taux3])
        result = where(etudiant, result_etudiant, result_non_etudiant)
        print(ressources)
        print(simulation.calculate('salaire_net', period.start.period('year').offset(-1))/12)
        print(simulation.calculate('rsa', period.start.period('year').offset(-1))/12)
        print(result_non_etudiant)
        print(result)
        return period, result



class rennes_metropole_transport_etudiant(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Calcul tarification solidaire"


    def function(self, simulation, period):
        period = period.this_month
        taux1= simulation.legislation_at(period.start).rennesmetropole.tarification_solidaire.taux_reduction.taux1      
        taux2 = simulation.legislation_at(period.start).rennesmetropole.tarification_solidaire.taux_reduction.taux2
        taux3 = simulation.legislation_at(period.start).rennesmetropole.tarification_solidaire.taux_reduction.taux3
        
        #montant_bourse = simulation.calculate('bourse_enseignement_sup',)
        
        #echelon = simulation.calculate('echelon_bourse',period)
        echelon = 1
        print(echelon)
        result_etudiant = select([echelon >= 5,echelon >= 3, echelon >= 2], [taux1,taux2,taux3])
        return period, result_etudiant