from openfisca_france.model.base import Variable, Individu, Famille, MONTH


class titre_sejour(Variable):
    value_type = bool
    label ="Bénéficiaire d'un titre de séjour"
    entity = Individu
    definition_period = MONTH
    default_value = False


class refugie(Variable):
    value_type = bool
    label = "La personne dispose du statut de réfugié"
    entity = Individu
    definition_period = MONTH
    default_value = False


class apatride(Variable):
    value_type = bool
    label = "La personne est apatride"
    entity = Individu
    definition_period = MONTH
    default_value = False


class aide_menagere_fournie_caisse_retraite(Variable):
    value_type = bool
    label = "Bénéficiaire de prestations d’aide-ménagère servie par les caisses de retraite"
    entity = Individu
    definition_period = MONTH
    default_value = False


class beneficiaire_actp(Variable):
    value_type = bool
    label = "Bénéficiaire de l'Allocation compensatrice pour tierce personne"
    entity = Individu
    definition_period = MONTH
    default_value = False


class mtp(Variable):
    value_type = bool
    label ="Bénéficiaire de la Majoration Tierce Personne"
    entity = Individu
    definition_period = MONTH
    default_value = False


class beneficiaire_acfp(Variable):
    value_type = bool
    label ="Bénéficiaire de l'Allocation compensatrice pour frais professionnel"
    entity = Individu
    definition_period = MONTH
    default_value = False


class beneficiaire_complement_aeeh(Variable):
    value_type = bool
    label ="Bénéficiaire du complément à l'Allocation d'éducation de l'enfant handicapé"
    entity = Famille
    definition_period = MONTH
    default_value = False

class mtp(Variable):
    value_type = bool
    label ="Bénéficiaire de la Majoration Tierce Personne"
    entity = Individu
    definition_period = MONTH
    default_value = False


class station_debout_penible(Variable):
    value_type = bool
    label = "La station debout est pénible pour cet individu"
    entity = Individu
    definition_period = MONTH
    default_value = False


class refugie(Variable):
    value_type = bool
    label = "La personne est réfugié"
    entity = Individu
    definition_period = MONTH
    default_value = False

class apatride(Variable):
    value_type = bool
    label = "La personne est apatride"
    entity = Individu
    definition_period = MONTH
    default_value = False
