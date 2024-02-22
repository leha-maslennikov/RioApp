import sqlite3 as sq
import datetime
from typing import Type

#print(datetime.datetime.utcfromtimestamp(1705693235))
#print(datetime.timedelta(seconds=2147))

class KeyCharacter:
    id: int  
    guid: int
    name: str
    spec_id: int
    ilvl: int
    spec_id: int 
    covenant_id: int
    soulbind_id: int
    ID = 'id'
    GUID = 'guid'
    NAME = 'name'
    SPEC_ID = 'specID'
    ILVL = 'Ilvl'
    COVENANT_ID = 'CovenantID'
    SOULBIND_ID = 'SoulbindID'

class Key:
    id:int 
    inst: str
    affixes: str
    challenge_level: int
    date: str
    record_time: str
    timer_level: int
    characters: list[Type[KeyCharacter]]
    ID = 'id'
    INST = 'inst'
    AFFIXES = 'Affixes'
    CHALLENGE_LEVEL = 'ChallengeLevel'
    DATE = 'Date'
    RECORD_TIME = 'RecordTime'
    TIMER_LEVEL = 'TimerLevel'

class Character:
    guid: int
    name: str
    keys: list[Type[Key]]
    GUID = 'guid' 
    NAME = 'name'
    KEYS = 'keys'


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




class MythicData:
    MYTHIC = Table('mythic')
    MYTHIC_GUID = Table('mythic_guid')
    CHARACTERS = Table('characters')  

    def __init__(self) -> None:
        self.conn = sq.connect('data.db')
        self.cur = self.conn.cursor()

    def __del__(self) -> None:
        self.cur.close()
        self.conn.close()

    def create(self):
        '''
        DROP IF EXIST AND CREATE mythic, characters, mythic_guid
        Affixes ChallengeLevel Date RecordTime TimerLevel
        guid name specID CovenantID SoulbindID'''
        self.cur.execute('DROP TABLE IF EXISTS mythic')
        self.cur.execute('DROP TABLE IF EXISTS characters')
        self.cur.execute('DROP TABLE IF EXISTS mythic_guid')
        self.cur.execute(
            f'''
            CREATE TABLE mythic (
                {Key.ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                {Key.INST} TEXT,
                {Key.AFFIXES} TEXT,
                {Key.CHALLENGE_LEVEL} INTEGER,
                {Key.DATE} TEXT,
                {Key.RECORD_TIME} TEXT,
                {Key.TIMER_LEVEL} INTEGER
            )'''
        )
        self.cur.execute(
            f'''
            CREATE TABLE mythic_guid (
                {KeyCharacter.ID} INTEGER,  
                {KeyCharacter.GUID} INTEGER,
                {KeyCharacter.NAME} TEXT,
                {KeyCharacter.SPEC_ID} INTEGER,
                {KeyCharacter.ILVL} INTEGER,
                {KeyCharacter.COVENANT_ID} INTEGER, 
                {KeyCharacter.SOULBIND_ID} INTEGER
            )'''
        )
        self.cur.execute(
            f'''
            CREATE TABLE characters (
                {Character.GUID} INTEGER PRIMARY KEY,  
                {Character.NAME} TEXT,
                {Character.KEYS} TEXT
            )'''
        )

    def add_key(self, key: Type[Key]):
        '''key json added in db
        old:('{dung[key['MapID']]}', '{key['Affixes']}', {key['ChallengeLevel']}, '{datetime.datetime.utcfromtimestamp(int(key['Date']))}', '{datetime.timedelta(seconds=int(key['RecordTime']))}', {key['TimerLevel']})
        ({id}, {member['guid']}, '{member['name']}', {member['specID']}, {member['Ilvl']}, {member['CovenantID']}, {member['SoulbindID']})
        '''
        id = self.cur.execute(
            f'''
            INSERT INTO mythic({Key.ID},{Key.INST},{Key.AFFIXES},{Key.CHALLENGE_LEVEL},{Key.DATE},{Key.RECORD_TIME},{Key.TIMER_LEVEL}) VALUES
            ({key.id},{key.inst},{key.affixes},{key.challenge_level},{key.date},{key.record_time},{key.timer_level})
            '''
        ).lastrowid
        for member in key.characters:
            cmd = f'''
                INSERT INTO mythic_guid({KeyCharacter.ID}, {KeyCharacter.GUID}, {KeyCharacter.NAME}, {KeyCharacter.SPEC_ID}, {KeyCharacter.ILVL}, {KeyCharacter.COVENANT_ID}, {KeyCharacter.SOULBIND_ID}) VALUES
                ({member.id}, {member.guid}, {member.name}, {member.spec_id}, {member.ilvl}, {member.covenant_id}, {member.soulbind_id})
                    '''
            self.cur.execute(cmd)
            keys = self.cur.execute(f"SELECT {Character.KEYS} FROM characters WHERE {Character.GUID}={member.guid}").fetchone()
            if keys:
                self.cur.execute(
                    f'''UPDATE characters SET {Character.KEYS} = '{keys[0]+' '+str(id)}' WHERE {Character.guid}={member.guid}'''
                )
            else:
                self.cur.execute(
                    f'''INSERT INTO characters({Character.GUID}, {Character.NAME}, {Character.KEYS}) VALUES ({member.guid}, '{member.name}', '{id}')'''
                )

    def get_character_by_name(self, name: str):
        '''SELECT character whose nickname start with name'''
        res = self.cur.execute(
            f'''SELECT {Character.GUID}, {Character.NAME}, {Character.KEYS} FROM characters WHERE {Character.NAME} LIKE '{name}%' '''
        )
        res = []
        for i in res.fetchall():
            char = Character()
            char.guid = i[0]
            char.name = i[1]
            char.keys = i[2]
            res.append(char)
        return res
    

    def get_character_by_key_id(self, id):
        '''SELECT characters from key with id'''
        res = self.cur.execute(
            f'''SELECT * FROM mythic_guid WHERE {KeyCharacter.ID} = {id}'''
        )
        return res.fetchall() 
      

    def get_keys(self, offset, limit = 10):
        '''SELECT limit keys wit offset'''
        res = self.cur.execute(
            f'''SELECT * FROM mythic LIMIT {offset}, {limit} '''
        )
        keys = []
        for i in res.fetchall():
            key = Key()
            key.id = i[0]
            key.inst = i[1]
            key.affixes = i[2]
            key.challenge_level = i[3]
            key.date = i[4]
            key.record_time = i[5]
            key.timer_level = i[6]
            keys.append(key)
        return keys

