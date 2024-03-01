import flet as ft
import requests
from mythicdatabase import Character, Key, KeyCharacter, MDB

dung = {
    '2284' :	'Sanguine Depths',
    '2285' :	'Spires of Ascension',
    '2286' :	'The Necrotic Wake',
    '2287' : 	'Halls of Atonement',
    '2289' :	'Plaguefall',
    '2290' :	'Mists of Tirna Scithe',
    '2291' :	'De Other Side',
    '2293' :	'Theater of Pain',
    '2441' :	'Tazavesh the Veiled Market'
}

specialization = {	
    250 : ('Death Knight', 'assets\img\classes\dk.png', 'Blood', '', 't'),
    251 : ('Death Knight', 'assets\img\classes\dk.png', 'Frost', '', 'd'),
    252 : ('Death Knight', 'assets\img\classes\dk.png', 'Unholy', '', 'd'),
    77 : ('Demon Hunter', 'assets\img\classes\dh.png', 'Havoc', '', 'd'),
    581 : ('Demon Hunter', 'assets\img\classes\dh.png', 'Vengeance', '', 't'),
    102 : ('Druid', 'assets\img\classes\druid.png', 'Balance', '', 'd'),
    103 : ('Druid', 'assets\img\classes\druid.png', 'Feral', '', 'd'),
    104 : ('Druid', 'assets\img\classes\druid.png', 'Guardian', '', 't'),
    105 : ('Druid', 'assets\img\classes\druid.png', 'Restoration', '', 'h'),
    253 : ('Hunter', 'assets\img\classes\hunter.png', 'Beast Mastery', '', 'd'),
    254 : ('Hunter', 'assets\img\classes\hunter.png', 'Marksmanship', '', 'd'),
    255 : ('Hunter', 'assets\img\classes\hunter.png', 'Survival', '', 'd'),
    62 : ('Mage', 'assets\img\classes\mage.png', 'Arcane', '', 'd'),
    63 : ('Mage', 'assets\img\classes\mage.png', 'Fire', '', 'd'),
    64 : ('Mage', 'assets\img\classes\mage.png', 'Frost', '', 'd'),
    268 : ('Monk', 'assets\img\classes\monk.png', 'Brewmaster', '', 't'),
    270 : ('Monk', 'assets\img\classes\monk.png', 'Mistweaver', '', 'h'),
    269 : ('Monk', 'assets\img\classes\monk.png', 'Windwalker', '', 'd'),
    65 : ('Paladin', 'assets\img\classes\paladin.png', 'Holy', '', 'h'),
    66 : ('Paladin', 'assets\img\classes\paladin.png', 'Protection', '', 't'),
    70 : ('Paladin', 'assets\img\classes\paladin.png', 'Retribution', '', 'd'),
    256 : ('Priest', 'assets\img\classes\priest.png', 'Discipline', '', 'h'),
    257 : ('Priest', 'assets\img\classes\priest.png', 'Holy', '', 'h'),
    258 : ('Priest', 'assets\img\classes\priest.png', 'Shadow', '', 'd'),
    259 : ('Rogue', 'assets\img\classes\\rouge.png', 'Assassination', '', 'd'),
    260 : ('Rogue', 'assets\img\classes\\rouge.png', 'Outlaw', '', 'd'),
    261 : ('Rogue', 'assets\img\classes\\rouge.png', 'Subtlety', '', 'd'),
    262 : ('Shaman', 'assets\img\classes\sham.png', 'Elemental', '', 'd'),
    263 : ('Shaman', 'assets\img\classes\sham.png', 'Enhancement', '', 'd'),
    264 : ('Shaman', 'assets\img\classes\sham.png', 'Restoration', '', 'h'),
    65 : ('Warlock', 'assets\img\classes\lock.png', 'Affliction', '', 'd'),
    266 : ('Warlock', 'assets\img\classes\lock.png', 'Demonology', '', 'd'),
    267 : ('Warlock', 'assets\img\classes\lock.png', 'Destruction', '', 'd'),
    71 : ('Warrior', 'assets\img\classes\war.png', 'Arms', '', 'd'),
    72 : ('Warrior', 'assets\img\classes\war.png', 'Fury', '', 'd'),
    73 : ('Warrior', 'assets\img\classes\war.png', 'Protection', '', 't')
}

colors = {
    'Priest' : ft.colors.WHITE,
    'Warrior' : ft.colors.BROWN,
    'Shaman' : ft.colors.BLUE,
    'Death Knight' : ft.colors.RED,
    'Paladin' : ft.colors.PINK_200,
    'Demon Hunter' : ft.colors.PURPLE,
    'Warlock' : ft.colors.PURPLE_200,
    'Monk' : ft.colors.GREEN_ACCENT,
    'Rogue' : ft.colors.YELLOW,
    'Hunter' : ft.colors.GREEN,
    'Mage' : ft.colors.LIGHT_BLUE_200,
    'Druid' : ft.colors.ORANGE
}


class Specialization:
    _class: str
    spec: str
    class_img: str
    spec_img: str
    color: str
    role: str

    def __init__(self, spec_id: int, name: str) -> None:
        r = specialization[spec_id]
        self._class = r[0]
        self.class_img = r[1]
        self.spec = r[2]
        self.spec_img = r[3]
        self.color = colors[self._class]
        self.name = name
        self.role = r[4]

    def get_text(self):
        return ft.Row(
            [
                ft.Image(src = self.class_img, width=20),
                ft.Text(self.name, size=16, color=self.color)
                ]
            )
    
cahce = {}
def get_affix_img(affix: int):
    '''src to img'''
    if affix in cahce:
        return cahce[affix]
    res = requests.get(f'https://nether.wowhead.com/tooltip/affix/{affix}?dataEnv=1&locale=0')
    cahce[affix] = f'https://wow.zamimg.com/images/wow/icons/medium/{res.json()["icon"]}.jpg'
    return cahce[affix]

def get_score(level: int, record: int) -> int:
    return 30+5*level+int(level>3)*5+int(level>6)*5+int(level>9)*10 + 2.5*record - 3*(not record)

def count_score(char: Character, keys: list[Key]):
    insts = {
        'Sanguine Depths' : {},
        'Spires of Ascension' : {},
        'The Necrotic Wake' : {},
        'Halls of Atonement' : {},
        'Plaguefall' : {},
        'Mists of Tirna Scithe' : {},
        'De Other Side' : {},
        'Theater of Pain' : {},
        'Tazavesh the Veiled Market' : {}
    }
    for key in keys:
        for c in key.characters:
            if char.name == c.name:
                if c.spec_id not in insts[key.inst]:
                    k = Key()
                    k.score = 0
                    insts[key.inst][c.spec_id] = [k, k]
                if 'https://wow.zamimg.com/images/wow/icons/medium/ability_toughness.jpg' in key.affixes:
                    if insts[key.inst][c.spec_id][0].score < key.score:
                        insts[key.inst][c.spec_id][0] = key
                else:
                    if insts[key.inst][c.spec_id][1].score < key.score:
                        insts[key.inst][c.spec_id][1] = key
                continue
    spec_score = {}
    for inst, other in insts.items():
        bk1 = bk2 = 0
        for spec, k in other.items():
            if k[0].score > bk1:
                bk1 = k[0].score
            if k[1].score > bk2:
                bk2 = k[1].score
            score = [k[0].score, k[1].score]
            if spec not in spec_score:
                spec_score[spec] = 0
            spec_score[spec] += max(score)*1.5 + min(score)*0.5
        char.score += max(bk1, bk2)*1.5 + min(bk1, bk2)*0.5
    for spec, k in spec_score.items():
        s = Specialization(spec, char.name)
        if s.role == 'd':
            char.dps_score += k
        if s.role == 't':
            char.tank_score += k
        if s.role == 'h':
            char.heal_score += k
    return spec_score
