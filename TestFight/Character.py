# imports
import math


# Ability class
class Ability:

    def __init__(self, name, ability_score, is_save_prof, prof_bonus, ability_mod=None, save_mod=None):
        self.name = name
        self.ability_score = ability_score
        if ability_mod:
            self.ability_mod = ability_mod
        else:
            self.ability_mod = int(math.floor((ability_score - 10) / 2))
        self.is_save_prof = is_save_prof
        self.prof_bonus = prof_bonus
        if save_mod:
            self.save_mod = save_mod
        else:
            self.save_mod = self.ability_mod
            if is_save_prof:
                self.save_mod += self.prof_bonus

    def __str__(self):
        return '{}: score= {}; mod= {}; is save prof= {}; prof bonus= {}; saving throw mod= {}'.format(
            self.name, self.ability_score, self.ability_mod, self.is_save_prof, self.prof_bonus, self.save_mod)


# Skill Class
class Skill:

    def __init__(self, name, is_prof, prof_bonus, ability, ability_mod, total=0, misc_bonus=0):
        self.name = name
        self.is_prof = is_prof
        self.prof_bonus = prof_bonus
        self.ability = ability
        self.ability_mod = ability_mod
        self.misc_bonus = misc_bonus
        if total:
            self.total = total
        else:
            total += ability_mod
            if is_prof:
                total += prof_bonus
            total += misc_bonus
            self.total = total

    def __str__(self):
        return '{}: prof= {}; prof bonus= {}; ability= {}; ability mod= {}; skill total= {}'.format(
            self.name, self.is_prof, self.prof_bonus, self.ability, self.ability_mod, self.total)


# Character Class
class Character:
    name = None
    class_lvls = {}
    race = None
    background = None
    alignment = None
    player_name = None
    exp_points = 0

    inspiration = 0
    prof_bonus = 2
    prof_saving_throws = []
    prof_skills = []

    abilities = {
        'charisma': Ability('charisma', 10, 'charisma' in prof_saving_throws, prof_bonus),
        'constitution': Ability('constitution', 10, 'constitution' in prof_saving_throws, prof_bonus),
        'dexterity': Ability('dexterity', 10, 'dexterity' in prof_saving_throws, prof_bonus),
        'intelligence': Ability('intelligence', 10, 'intelligence' in prof_saving_throws, prof_bonus),
        'strength': Ability('strength', 10, 'strength' in prof_saving_throws, prof_bonus),
        'wisdom': Ability('wisdom', 10, 'wisdom' in prof_saving_throws, prof_bonus)
    }

    skills = {
        'acrobatics': Skill('acrobatics', 'acrobatics' in prof_skills, prof_bonus,
                            'dexterity', abilities['dexterity'].ability_mod),
        'animal_handling': Skill('animal_handling', 'animal_handling' in prof_skills, prof_bonus, 'wisdom',
                                 abilities['wisdom'].ability_mod),
        'arcana': Skill('arcana', 'arcana' in prof_skills, prof_bonus, 'intelligence',
                        abilities['intelligence'].ability_mod),
        'athletics': Skill('athletics', 'athletics' in prof_skills, prof_bonus, 'strength',
                           abilities['strength'].ability_mod),
        'deception': Skill('deception', 'deception' in prof_skills, prof_bonus, 'charisma',
                           abilities['charisma'].ability_mod),
        'history': Skill('history', 'history' in prof_skills, prof_bonus, 'intelligence',
                         abilities['intelligence'].ability_mod),
        'insight': Skill('insight', 'insight' in prof_skills, prof_bonus, 'wisdom',
                         abilities['wisdom'].ability_mod),
        'intimidation': Skill('intimidation', 'intimidation' in prof_skills, prof_bonus, 'charisma',
                              abilities['charisma'].ability_mod),
        'investigation': Skill('investigation', 'investigation' in prof_skills, prof_bonus, 'intelligence',
                               abilities['intelligence'].ability_mod),
        'medicine': Skill('medicine', 'medicine' in prof_skills, prof_bonus, 'wisdom',
                          abilities['wisdom'].ability_mod),
        'nature': Skill('nature', 'nature' in prof_skills, prof_bonus, 'intelligence',
                        abilities['intelligence'].ability_mod),
        'perception': Skill('perception', 'perception' in prof_skills, prof_bonus, 'wisdom',
                            abilities['wisdom'].ability_mod),
        'persuasion': Skill('persuasion', 'persuasion' in prof_skills, prof_bonus, 'charisma',
                            abilities['charisma'].ability_mod),
        'religion': Skill('religion', 'religion' in prof_skills, prof_bonus, 'intelligence',
                          abilities['intelligence'].ability_mod),
        'sleight_of_hand': Skill('sleight_of_hand', 'sleight_of_hand' in prof_skills, prof_bonus, 'dexterity',
                                 abilities['dexterity'].ability_mod),
        'stealth': Skill('stealth', 'stealth' in prof_skills, prof_bonus, 'dexterity',
                         abilities['dexterity'].ability_mod),
        'survival': Skill('survival', 'survival' in prof_skills, prof_bonus, 'wisdom',
                          abilities['wisdom'].ability_mod)
    }

    languages = ['common']

    armor_class = 10
    initiative = abilities['dexterity'].ability_mod
    speed = 30

    hp = {
        'maximum': 12,
        'current': 12,
        'temporary': 0,
        'hit_die': {'d6': 0, 'd8': 0, 'd10': 0, 'd12': 0},
        'hit_die_used': {'d6': 0, 'd8': 0, 'd10': 0, 'd12': 0},
        'death_save_successes': 0,
        'death_save_fails': 0
    }

    attacks = None

    spellcasting = None

    equipment = {}

    coins = {
        'copper': 0,
        'silver': 0,
        'electrum': 0,
        'gold': 0,
        'platinum': 0
    }

    traits = {
        'personality': '',
        'ideals': '',
        'bonds': '',
        'flaws': ''
    }

    features = {}

    age = None
    height = None
    weight = None
    eyes = None
    skin = None
    hair = None

    appearance = None
    backstory = None
    allies_orgs = None
    allies_orgs_name = None
    allies_orgs_symbol = None
    features_additional = None
    treasure = None

    spellcasting_classes = []
    spellcasting_abilities = []
    spell_save_dc = 10
    spell_attack_bonus = 0

    # dicts of number of slots (value) per spell level (key)
    spell_slots_total = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    spell_slots_used = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    # dicts of number of total spells (value) per spell level (key)
    spells_known_total = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    spells_prepared_total = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    # dicts of lists of spells (value) per spell level (key)
    spells_known = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
    spells_prepared = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}


    def __init__(self, source_flag=None, source=None):
        if source_flag == 'pdf':        # if source is a pdf, then do this
            self.update_char_from_pdf(source)
        elif source_flag == 'xml':      # if source is FG, then do this
            self.update_char_from_xml(source)


    # pdf is a dict
    def update_char_from_pdf(self, pdf):

        for k,v in pdf.items():
            print(k, v)

        self.name = pdf['CharacterName']
        self.class_lvls = pdf['ClassLevel']
        self.race = pdf['Race ']
        self.background = pdf['Background']
        self.alignment = pdf['Alignment']
        self.player_name = pdf['PlayerName']
        self.exp_points = pdf['XP']

        self.inspiration = pdf['Inspiration']
        self.prof_bonus = pdf['ProfBonus']
        # TODO - remove, use bools not a list
        self.prof_saving_throws = []
        self.prof_skills = []

        # ST STR - box 11, ST DEX - box 18, ST CON - box 19
        # ST INT - box 20, ST WIS - box 21, ST CHA - box 22
        is_prof_st_cha = pdf['Check Box 22']
        is_prof_st_con = pdf['Check Box 19']
        is_prof_st_dex = pdf['Check Box 18']
        is_prof_st_int = pdf['Check Box 20']
        is_prof_st_str = pdf['Check Box 11']
        is_prof_st_wis = pdf['Check Box 21']

        self.abilities = {
            'charisma': Ability('charisma', pdf['CHA'], is_prof_st_cha, self.prof_bonus, pdf['CHamod'], pdf['ST Charisma']),
            'constitution': Ability('constitution', pdf['CON'], is_prof_st_con, self.prof_bonus, pdf['CONmod'], pdf['ST Constitution']),
            'dexterity': Ability('dexterity', pdf['DEX'], is_prof_st_dex, self.prof_bonus, pdf['DEXmod '], pdf['ST Dexterity']),
            'intelligence': Ability('intelligence', pdf['INT'], is_prof_st_int, self.prof_bonus, pdf['INTmod'], pdf['ST Intelligence']),
            'strength': Ability('strength', pdf['STR'], is_prof_st_str, self.prof_bonus, pdf['STRmod'], pdf['ST Strength']),
            'wisdom': Ability('wisdom', pdf['WIS'], is_prof_st_wis, self.prof_bonus, pdf['WISmod'], pdf['ST Wisdom'])
        }

        is_prof_acrobatics = pdf['Check Box 23']
        is_prof_animal_handling = pdf['Check Box 24']
        is_prof_arcana = pdf['Check Box 25']
        is_prof_athletics = pdf['Check Box 26']
        is_prof_deception = pdf['Check Box 27']
        is_prof_history = pdf['Check Box 28']
        is_prof_insight = pdf['Check Box 29']
        is_prof_intimidation = pdf['Check Box 30']
        is_prof_investigation = pdf['Check Box 31']
        is_prof_medicine = pdf['Check Box 32']
        is_prof_nature = pdf['Check Box 33']
        is_prof_perception = pdf['Check Box 34']
        is_prof_performance = pdf['Check Box 35']
        is_prof_persuasion = pdf['Check Box 36']
        is_prof_religion = pdf['Check Box 37']
        is_prof_sleight_of_hand = pdf['Check Box 38']
        is_prof_stealth = pdf['Check Box 39']
        is_prof_survival = pdf['Check Box 40']

        self.skills = {
            'acrobatics': Skill('acrobatics', is_prof_acrobatics, self.prof_bonus,
                                'dexterity', self.abilities['dexterity'].ability_mod, pdf['Acrobatics']),      # box 23
            'animal_handling': Skill('animal_handling', is_prof_animal_handling, self.prof_bonus, 'wisdom',
                                     self.abilities['wisdom'].ability_mod, pdf['Animal']),      # box 24
            'arcana': Skill('arcana', is_prof_arcana, self.prof_bonus, 'intelligence',
                            self.abilities['intelligence'].ability_mod, pdf['Arcana']),      # box 25
            'athletics': Skill('athletics', is_prof_athletics, self.prof_bonus, 'strength',
                               self.abilities['strength'].ability_mod, pdf['Athletics']),      # box 26
            'deception': Skill('deception', is_prof_deception, self.prof_bonus, 'charisma',
                               self.abilities['charisma'].ability_mod, pdf['Deception ']),      # box 27
            'history': Skill('history', is_prof_history, self.prof_bonus, 'intelligence',
                             self.abilities['intelligence'].ability_mod, pdf['History ']),      # box 28
            'insight': Skill('insight', is_prof_insight, self.prof_bonus, 'wisdom',
                             self.abilities['wisdom'].ability_mod, pdf['Insight']),      # box 29
            'intimidation': Skill('intimidation', is_prof_intimidation, self.prof_bonus, 'charisma',
                                  self.abilities['charisma'].ability_mod, pdf['Intimidation']),      # box 30
            'investigation': Skill('investigation', is_prof_investigation, self.prof_bonus, 'intelligence',
                                   self.abilities['intelligence'].ability_mod, pdf['Investigation ']),      # box 31
            'medicine': Skill('medicine', is_prof_medicine, self.prof_bonus, 'wisdom',
                              self.abilities['wisdom'].ability_mod, pdf['Medicine']),      # box 32
            'nature': Skill('nature', is_prof_nature, self.prof_bonus, 'intelligence',
                            self.abilities['intelligence'].ability_mod, pdf['Nature']),      # box 33
            'perception': Skill('perception', is_prof_perception, self.prof_bonus, 'wisdom',
                                self.abilities['wisdom'].ability_mod, pdf['Perception ']),      # box 34
            'performance': Skill('performance', is_prof_performance, self.prof_bonus, 'charisma',
                                 self.abilities['charisma'].ability_mod, pdf['Performance']),      # box 35
            'persuasion': Skill('persuasion', is_prof_persuasion, self.prof_bonus, 'charisma',
                                self.abilities['charisma'].ability_mod, pdf['Persuasion']),      # box 36
            'religion': Skill('religion', is_prof_religion, self.prof_bonus, 'intelligence',
                              self.abilities['intelligence'].ability_mod, pdf['Religion']),      # box 37
            'sleight_of_hand': Skill('sleight_of_hand', is_prof_sleight_of_hand, self.prof_bonus, 'dexterity',
                                     self.abilities['dexterity'].ability_mod, pdf['SleightofHand']),      # box 38
            'stealth': Skill('stealth', is_prof_stealth, self.prof_bonus, 'dexterity',
                             self.abilities['dexterity'].ability_mod, pdf['Stealth ']),      # box 39
            'survival': Skill('survival', is_prof_survival, self.prof_bonus, 'wisdom',
                              self.abilities['wisdom'].ability_mod, pdf['Survival'])      # box 40
        }

        self.languages = pdf['ProficienciesLang']

        self.armor_class = pdf['AC']
        self.initiative = pdf['Initiative']
        self.speed = pdf['Speed']

        death_save_successes = pdf['Check Box 12'] + pdf['Check Box 13'] + pdf['Check Box 14']
        death_save_fails = pdf['Check Box 15'] + pdf['Check Box 16'] + pdf['Check Box 17']

        self.hp = {
            'maximum': pdf['HPMax'],
            'current': pdf['HPCurrent'],
            'temporary': pdf['HPTemp'],
            'hit_die': {'d6': 0, 'd8': 0, 'd10': 0, 'd12': 0},
            'hit_die_used': {'d6': 0, 'd8': 0, 'd10': 0, 'd12': 0},
            'death_save_successes': death_save_successes,        # boxes 12-14
            'death_save_fails': death_save_fails            # boxes 15-17
        }

        self.attacks = pdf['Wpn Name']

        self.spellcasting = pdf['AttacksSpellcasting']

        self.equipment = pdf['Equipment']

        self.coins = {
            'copper': pdf['CP'],
            'silver': pdf['SP'],
            'electrum': pdf['EP'],
            'gold': pdf['GP'],
            'platinum': pdf['PP']
        }

        self.traits = {
            'personality': pdf['PersonalityTraits '],
            'ideals': pdf['Ideals'],
            'bonds': pdf['Bonds'],
            'flaws': pdf['Flaws']
        }

        self.features = pdf['Features and Traits']

        self.age = pdf['Age']
        self.height = pdf['Height']
        self.weight = pdf['Weight']
        self.eyes = pdf['Eyes']
        self.skin = pdf['Skin']
        self.hair = pdf['Hair']

        self.appearance = pdf['CHARACTER IMAGE']
        self.backstory = pdf['Backstory']
        self.allies_orgs = pdf['Allies']
        self.allies_orgs_name = pdf['FactionName']
        self.allies_orgs_symbol = pdf['Faction Symbol Image']
        self.features_additional = pdf['Feat+Traits']
        self.treasure = pdf['Treasure']

        self.spellcasting_classes = pdf['Spellcasting Class 2']
        self.spellcasting_abilities = pdf['SpellcastingAbility 2']
        self.spell_save_dc = pdf['SpellSaveDC  2']
        self.spell_attack_bonus = pdf['SpellAtkBonus 2']

        # dicts of number of slots (value) per spell level (key)
        self.spell_slots_total = {
            1: pdf['SlotsTotal 19'],
            2: pdf['SlotsTotal 20'],
            3: pdf['SlotsTotal 21'],
            4: pdf['SlotsTotal 22'],
            5: pdf['SlotsTotal 23'],
            6: pdf['SlotsTotal 24'],
            7: pdf['SlotsTotal 25'],
            8: pdf['SlotsTotal 26'],
            9: pdf['SlotsTotal 27']
        }
        self.spell_slots_used = {
            1: pdf['SlotsRemaining 19'],
            2: pdf['SlotsRemaining 20'],
            3: pdf['SlotsRemaining 21'],
            4: pdf['SlotsRemaining 22'],
            5: pdf['SlotsRemaining 23'],
            6: pdf['SlotsRemaining 24'],
            7: pdf['SlotsRemaining 25'],
            8: pdf['SlotsRemaining 26'],
            9: pdf['SlotsRemaining 27']
        }

        # dicts of number of total spells (value) per spell level (key)
        self.spells_known_total = {
            0: 0,   # 1014, 1016, 1017, 1018, 1019, 1020, 1021, 1022
            1: 0,   # 1015, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033
            2: 0,   # 1046, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045
            3: 0,   # 1048, 1047, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059
            4: 0,   # 1061, 1060, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072
            5: 0,   # 1074, 1073, 1075, 1076, 1077, 1078, 1079, 1080, 1081
            6: 0,   # 1083, 1082, 1084, 1085, 1086, 1087, 1088, 1089, 1090
            7: 0,   # 1092, 1091, 1093, 1094, 1095, 1096, 1097, 1098, 1099
            8: 0,   # 10101, 10100, 10102, 10103, 10104, 10105, 10106
            9: 0    # 10108, 10107, 10109, 101010, 101011, 101012, 101013
        }
        self.spells_prepared_total = {
            1: 0,   # 251, 309, 3010, 3011, 3012, 3013, 3014, 3015, 3016, 3017, 3018, 3019
            2: 0,   # 313, 310, 3020, 3021, 3022, 3023, 3024, 3025, 3026, 3027, 3028, 3029, 3030
            3: 0,   # 314, 315, 3031, 3032, 3033, 3034, 3035, 3036, 3037, 3038, 3039, 3040, 3041
            4: 0,   # 317, 316, 3042, 3043, 3044, 3045, 3046, 3047, 3048, 3049, 3050, 3051, 3052
            5: 0,   # 319, 318, 3053, 3054, 3055, 3056, 3057, 3058, 3059
            6: 0,   # 321, 320, 3060, 3061, 3062, 3063, 3064, 3065, 3066
            7: 0,   # 323, 322, 3067, 3068, 3069, 3070, 3071, 3072, 3073
            8: 0,   # 325, 324, 3074, 3075, 3076, 3077, 3078
            9: 0    # 327, 326, 3079, 3080, 3081, 3082, 3082
        }

        # dicts of lists of spells (value) per spell level (key)
        self.spells_known = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: []}
        self.spells_prepared = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: []}


    def update_char_from_xml(self, xml):
        self.name = xml
        print(xml)
        print('------------')

# c = Character('pdf')
# print(list(c.skills.values()))
# for s in c.abilities.values():
#     print(s)

