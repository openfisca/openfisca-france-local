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

        salaire =  simulation.compute('salaire_net', period)
        salaire_cumul=self.sum_by_entity(salaire, entity = 'famille')

        seuil_evolutif=(1+individu_en_couple*(0.5+nombre_enfants*0.3))

        print(taux3)

        result = select([salaire_cumul <= seuil1*seuil_evolutif,salaire_cumul <= seuil2*seuil_evolutif, salaire_cumul <= seuil3*seuil_evolutif], [taux1,taux2,taux3])
        # import ipdb
        # ipdb.set_trace()

 
        return period, result

