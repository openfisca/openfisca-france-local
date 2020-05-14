 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, FoyerFiscal, Menage, MONTH, YEAR

code_communes = [
    b'31003', # Aigrefeuille
    b'31022', # Aucamville
    b'31025', # Aureville
    b'31032', # Aussonne
    b'31035', # Auzeville-Tolosane
    b'31036', # Auzielle
    b'31004', # Ayguesvives
    b'31044', # Balma
    b'31048', # Baziège
    b'31053', # Beaupuy
    b'31056', # Beauzelle
    b'31057', # Belberaud
    b'31058', # Belbèze-de-Lauragais
    b'31069', # Blagnac
    b'31075', # Bonrepos-sur-Aussonnelle
    b'31087', # Bragayrac
    b'31088', # Brax
    b'31091', # Bruguières
    b'31113', # Castanet-Tolosan
    b'31116', # Castelginest
    b'31117', # Castelmaurou
    b'31148', # Clermont-le-Fort
    b'31149', # Colomiers
    b'31150', # Cornebarrieu
    b'31151', # Corronsac
    b'31157', # Cugnaux
    b'31161', # Deyme
    b'31162', # Donneville
    b'31163', # Drémil-Lafage
    b'31165', # Eaunes
    b'31166', # Empeaux
    b'31169', # Escalquens
    b'31171', # Espanès
    b'31182', # Fenouillet
    b'31184', # Flourens
    b'31186', # Fonbeauzard
    b'31187', # Fonsorbes
    b'31192', # Fourquevaux
    b'31203', # Frouzins
    b'31205', # Gagnac-sur-Garonne
    b'31227', # Goyrans
    b'31230', # Gratentour
    b'31240', # Issus
    b'31561', # L'Union
    b'31526', # La Salvetat-Saint-Gilles
    b'31248', # Labarthe-sur-Lèze
    b'31249', # Labastide-Beauvoir
    b'31253', # Labastidette
    b'31254', # Labège
    b'31259', # Lacroix-Falgarde
    b'31269', # Lamasquère
    b'31273', # Lapeyrouse-Fossat
    b'31282', # Launaguet
    b'31284', # Lauzerville
    b'31287', # Lavernose-Lacasse
    b'31181', # Le Fauga
    b'31293', # Lespinasse
    b'31340', # Mervilla
    b'31351', # Mondonville
    b'31352', # Mondouzil
    b'31355', # Mons
    b'31364', # Montberon
    b'31366', # Montbrun-Lauragais
    b'31381', # Montgiscard
    b'31384', # Montlaur
    b'31389', # Montrabé
    b'31395', # Muret
    b'31401', # Noueilles
    b'31402', # Odars
    b'31409', # Péchabou
    b'31410', # Pechbonnieu
    b'31411', # Pechbusque
    b'31417', # Pibrac
    b'31418', # Pin-Balma
    b'31421', # Pins-Justaret
    b'31420', # Pinsaguel
    b'31424', # Plaisance-du-Touch
    b'31429', # Pompertuzat
    b'31433', # Portet-sur-Garonne
    b'31437', # Pouze
    b'31445', # Quint-Fonsegrives
    b'31446', # Ramonville-Saint-Agne
    b'31448', # Rebigue
    b'31458', # Roques
    b'31460', # Roquettes
    b'31462', # Rouffiac-Tolosan
    b'31464', # Sabonnères
    b'31466', # Saiguède
    b'31467', # Saint-Alban
    b'31475', # Saint-Clar-de-Rivière
    b'31484', # Saint-Geniès-Bellevue
    b'31486', # Saint-Hilaire
    b'31488', # Saint-Jean
    b'31490', # Saint-Jory
    b'31497', # Saint-Loup-Cammas
    b'31499', # Saint-Lys
    b'31506', # Saint-Orens-de-Gameville
    b'31518', # Saint-Thomas
    b'31533', # Saubens
    b'31541', # Seilh
    b'31547', # Seysses
    b'31555', # Toulouse
    b'31557', # Tournefeuille
    b'31568', # Varennes
    b'31575', # Vieille-Toulouse
    b'31578', # Vigoulet-Auzil
    b'31580', # Villate
    b'31588', # Villeneuve-Tolosane
]

class tisseo_ressort_territorial(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = u"Indicatrice du ressort territorial de Tisséo"

    def formula(menage, period):
        depcom = menage('depcom', period)
        return sum([depcom == code for code in code_communes])
