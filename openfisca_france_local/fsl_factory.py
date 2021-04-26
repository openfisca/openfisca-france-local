# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Menage, MONTH, not_
from openfisca_core import reforms
from numpy.core.defchararray import startswith


def fsl_factory_departement(prefix, dlabel, code_insee_departement, metropole_siren_exclusion=None):
    class NewFSLClass(Variable):
        value_type = bool
        entity = Menage
        definition_period = MONTH
        label = u"Ménage éligible à l'aide au maintien du FSL du département %s" % dlabel

        def formula(menage, period):
            in_departement = startswith(menage('depcom', period), code_insee_departement)
            if metropole_siren_exclusion is not None:
                in_epci = menage("menage_dans_epci_siren_%i" % metropole_siren_exclusion, period)
                return in_departement * not_(in_epci)
            else:
                return in_departement

    NewFSLClass.__name__ = "%s_fonds_solidarite_logement_aide_maintien_eligibilite" % prefix
    return NewFSLClass


def fsl_factory_metropole(prefix, mlabel, metropole_siren_limitation):
    class NewFSLClass(Variable):
          value_type = bool
          entity = Menage
          definition_period = MONTH
          label = u"Ménage éligible à l'aide au maintien du FSL %s" % mlabel

          def formula(menage, period):
              return menage("menage_dans_epci_siren_%i" % metropole_siren_limitation, period)

    NewFSLClass.__name__ = "%s_metropole_fonds_solidarite_logement_aide_maintien_eligibilite" % prefix
    return NewFSLClass


class fsl_reform(reforms.Reform):
    def apply(self):
        self.add_variable(fsl_factory_departement('ain', 'de l’Ain', b'01'))
        self.add_variable(fsl_factory_departement('aisne', 'de l’Aisne', b'02'))
        self.add_variable(fsl_factory_departement('allier', 'de l’Allier', b'03'))
        self.add_variable(fsl_factory_departement('alpes_de_haute_provence', 'des Alpes-de-Haute-Provence', b'04'))
        self.add_variable(fsl_factory_departement('hautes_alpes', 'des Hautes Alpes', b'05'))
        self.add_variable(fsl_factory_departement('alpes_maritimes', 'des Alpes Maritimes', b'06', 200030195))
        self.add_variable(fsl_factory_metropole('nice', 'de la Métropole Nice Côte d’Azur', 200030195))
        self.add_variable(fsl_factory_departement('ardeche', 'de l’Ardèche', b'07'))
        self.add_variable(fsl_factory_departement('ardennes', 'de l’Ardennes', b'08'))
        self.add_variable(fsl_factory_departement('ariege', 'de l’Ariège', b'09'))
        self.add_variable(fsl_factory_departement('aube', 'de ’Aube', b'10'))
        self.add_variable(fsl_factory_departement('aude', 'de l’Aude', b'11'))
        self.add_variable(fsl_factory_departement('aveyron', 'de l’Aveyron', b'12'))
        self.add_variable(fsl_factory_departement('bouches_du_rhone', 'Des Bouches-du-Rhône', b'13', 200054807))
        self.add_variable(fsl_factory_metropole('marseille', 'de la Métropole d’Aix-Marseille-Provence', 200054807))
        self.add_variable(fsl_factory_departement('calvados', 'du Calvados', b'14'))
        self.add_variable(fsl_factory_departement('cantal', 'du Cantal', b'15'))
        self.add_variable(fsl_factory_departement('charente', 'de Charente', b'16'))
        self.add_variable(fsl_factory_departement('charente_maritime', 'de Charente-Maritime', b'17'))
        self.add_variable(fsl_factory_departement('cher', 'du Cher', b'18'))
        self.add_variable(fsl_factory_departement('correze', 'de Corrèze', b'19'))
        self.add_variable(fsl_factory_departement('cotes_d_or', 'de la Côte-d’Or', b'21', 242100410))
        self.add_variable(fsl_factory_metropole('dijon', 'de Dijon Métropole', 242100410))
        self.add_variable(fsl_factory_departement('creuse', 'de la Creuse', b'23'))
        self.add_variable(fsl_factory_departement('dordogne', 'de la Dordogne', b'24'))
        self.add_variable(fsl_factory_departement('doubs', 'du Doubs', b'25'))
        self.add_variable(fsl_factory_departement('drome', 'de la Drôme', b'26'))
        self.add_variable(fsl_factory_departement('eure', 'de l’Eure', b'27'))
        self.add_variable(fsl_factory_departement('finistere', 'du Finistère', b'29', 242900314))
        self.add_variable(fsl_factory_metropole('brest', 'de Brest Métropole', 242900314))
        self.add_variable(fsl_factory_departement('gard', 'du Gard', b'30'))
        self.add_variable(fsl_factory_departement('haute_garonne', 'de la Haute-Garonne', b'31', 243100518))
        self.add_variable(fsl_factory_metropole('toulouse', 'de Toulouse Métropole', 243100518))
        self.add_variable(fsl_factory_departement('gers', 'du Gers', b'32'))
        self.add_variable(fsl_factory_departement('gironde', 'de la Gironde', b'33', 243300316))
        self.add_variable(fsl_factory_metropole('bordeaux', 'de Bordeaux Métropole', 243300316))
        self.add_variable(fsl_factory_departement('herault', 'de l’Hérault', b'34', 243400017))
        self.add_variable(fsl_factory_metropole('montpellier', 'de la Montpellier Méditerranée Métropole', 243400017))
        self.add_variable(fsl_factory_departement('ille_et_vilaine', 'd’Ille-et-Vilaine', b'35', 243500139))
        self.add_variable(fsl_factory_metropole('rennes', 'de Rennes Métropole', 243500139))
        self.add_variable(fsl_factory_departement('indre', 'de l’Indre', b'36'))
        self.add_variable(fsl_factory_departement('indre_et_loire', 'de l’Indre-et-Loire', b'37', 243700754))
        self.add_variable(fsl_factory_metropole('tours', 'de Tours Métropole Val de Loire', 243700754))
        self.add_variable(fsl_factory_departement('isere', 'd’Isère', b'38', 200040715))
        self.add_variable(fsl_factory_metropole('grenoble', 'de Grenoble-Alpes-Métropole', 200040715))
        self.add_variable(fsl_factory_departement('jura', 'du Jura', b'39'))
        self.add_variable(fsl_factory_departement('landes', 'des Landes', b'40'))
        self.add_variable(fsl_factory_departement('loir_et_cher', 'du Loir-et-Cher', b'41'))
        self.add_variable(fsl_factory_departement('loire', 'de la Loire', b'42', 244200770))
        self.add_variable(fsl_factory_metropole('saint_etienne', 'de Saint-Etienne Métropole', 244200770))
        self.add_variable(fsl_factory_departement('haute_loire', 'de la Haute-Loire', b'43'))
        self.add_variable(fsl_factory_departement('loire_atlantique', 'de la Loire Atlantique', b'44', 244400404))
        self.add_variable(fsl_factory_metropole('nantes', 'de Nantes Métropole', 244400404))
        self.add_variable(fsl_factory_departement('loiret', 'du Loiret', b'45', 244500468))
        self.add_variable(fsl_factory_metropole('orleans', 'de Orléans Métropole', 244500468))
        self.add_variable(fsl_factory_departement('lot', 'du Lot', b'46'))
        self.add_variable(fsl_factory_departement('lot_et_garonne', 'du Lot-et-Garonne', b'47'))
        self.add_variable(fsl_factory_departement('lozere', 'de la Lozère', b'48'))
        self.add_variable(fsl_factory_departement('maine_et_loire', 'du Maine-et-Loire', b'49'))
        self.add_variable(fsl_factory_departement('manche', 'de la Manche', b'50'))
        self.add_variable(fsl_factory_departement('marne', 'de la Marne', b'51'))
        self.add_variable(fsl_factory_departement('haute_marne', 'de la Haute-Marne', b'52'))
        self.add_variable(fsl_factory_departement('mayenne', 'de la Mayenne', b'53'))
        self.add_variable(fsl_factory_departement('meurthe_et_moselle', 'de la Meurthe-et-Moselle', b'54', 245400676))
        self.add_variable(fsl_factory_metropole('nancy', 'de la Métropole du Grand Nancy', 245400676))
        self.add_variable(fsl_factory_departement('meuse', 'de la Meuse', b'55'))
        self.add_variable(fsl_factory_departement('morbihan', 'du Morbihan', b'56'))
        self.add_variable(fsl_factory_departement('moselle', 'de la Moselle', b'57', 200039865))
        self.add_variable(fsl_factory_metropole('metz', 'de Metz Métropole', 200039865))
        self.add_variable(fsl_factory_departement('nievre', 'de la Nièvre', b'58'))
        self.add_variable(fsl_factory_departement('nord', 'du Nord', b'59', 245900410))
        self.add_variable(fsl_factory_metropole('lille', 'de la Métropole Européenne de Lille', 245900410))
        self.add_variable(fsl_factory_departement('oise', 'de l’Oise', b'60'))
        self.add_variable(fsl_factory_departement('orne', 'de l’Orne', b'61'))
        self.add_variable(fsl_factory_departement('pas_de_calais', 'du Pas-de-Calais', b'62'))
        self.add_variable(fsl_factory_departement('puy_de_dôme', 'du Puy-de-Dôme', b'63', 246300701))
        self.add_variable(fsl_factory_metropole('clermond_ferrand', 'de Clermont Auvergne Métropole', 246300701))
        self.add_variable(fsl_factory_departement('pyrenees_atlantiques', 'des Pyrénées-Atlantiques', b'64'))
        self.add_variable(fsl_factory_departement('hautes_pyrenees', 'des Hautes-Pyrénées', b'65'))
        self.add_variable(fsl_factory_departement('pyrenees_orientables', 'des Pyrénées-Orientales', b'66'))
        self.add_variable(fsl_factory_departement('bas_rhin', 'du Bas-Rhin', b'67', 246700488))
        self.add_variable(fsl_factory_metropole('strasbourg', 'de l’Eurométropole de Strasbourg', 246700488))
        self.add_variable(fsl_factory_departement('haut_rhin', 'du Haut-Rhin', b'68'))
        self.add_variable(fsl_factory_departement('rhone', 'du Rhône', b'69', 200046977))
        self.add_variable(fsl_factory_metropole('lyon', 'de la Métropole de Lyon', 200046977))
        self.add_variable(fsl_factory_departement('haute_saone', 'de la Haute-Saône', b'70'))
        self.add_variable(fsl_factory_departement('saone_et_loire', 'de la Saône-et-Loire', b'71'))
        self.add_variable(fsl_factory_departement('sarthe', 'de la Sarthe', b'72'))
        self.add_variable(fsl_factory_departement('savoie', 'de la Savoie', b'73'))
        self.add_variable(fsl_factory_departement('haute_savoie', 'de la Haute-Savoie', b'74'))
        self.add_variable(fsl_factory_departement('paris', 'de Paris', b'75'))
        self.add_variable(fsl_factory_departement('seine_maritime', 'de Seine-Maritime', b'76', 200023414))
        self.add_variable(fsl_factory_metropole('rouan', 'de la Métropole Rouen Normandie', 200023414))
        self.add_variable(fsl_factory_departement('seine_et_marne', 'de Seine-et-Marne', b'77'))
        self.add_variable(fsl_factory_departement('yvelines', 'des Yvelines', b'78'))
        self.add_variable(fsl_factory_departement('deux_sevres', 'des Deux-Sèvres', b'79'))
        self.add_variable(fsl_factory_departement('somme', 'de la Somme', b'80'))
        self.add_variable(fsl_factory_departement('tarn', 'du Tarn', b'81'))
        self.add_variable(fsl_factory_departement('tarn_et_garonne', 'du Tarn-et-Garonne', b'82'))
        self.add_variable(fsl_factory_departement('var', 'du Var', b'83', 248300543))
        self.add_variable(fsl_factory_metropole('toulon', 'de la Métropole Toulon-Provence-Méditerranée', 248300543))
        self.add_variable(fsl_factory_departement('vaucluse', 'du Vaucluse', b'84'))
        self.add_variable(fsl_factory_departement('vendee', 'de la Vendée', b'85'))
        self.add_variable(fsl_factory_departement('vienne', 'de la Vienne', b'86'))
        self.add_variable(fsl_factory_departement('haute_vienne', 'de la Haute-Vienne', b'87'))
        self.add_variable(fsl_factory_departement('vosges', 'des Vosges', b'88'))
        self.add_variable(fsl_factory_departement('yonne', 'de l’Yonne', b'89'))
        self.add_variable(fsl_factory_departement('terrtoire_de_belfort', 'du Territoire de Belfort', b'90'))
        self.add_variable(fsl_factory_departement('essonne', 'de l’Essonne', b'91'))
        self.add_variable(fsl_factory_departement('hauts_de_seine', 'des Hauts-de-Seine', b'92'))
        self.add_variable(fsl_factory_departement('seine_saint_denis', 'de Seine-Saint-Denis', b'93'))
        self.add_variable(fsl_factory_departement('val_de_marne', 'du Val-de-Marne', b'94'))
        self.add_variable(fsl_factory_departement('val_d_oise', 'du Val d’Oise', b'95'))
        self.add_variable(fsl_factory_departement('guadeloupe', 'de la Guadeloupe', b'971'))
        self.add_variable(fsl_factory_departement('martinique', 'de la Martinique', b'972'))
        self.add_variable(fsl_factory_departement('guyane', 'de la Guyane', b'973'))
        self.add_variable(fsl_factory_departement('la_reunion', 'de la Réunion', b'974'))
        self.add_variable(fsl_factory_departement('corse_du_sud', 'de la Corse-du-Sud', b'2A'))
        self.add_variable(fsl_factory_departement('haute_corse', 'de la Haute-Corse', b'2B'))
