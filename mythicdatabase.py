from threading import Thread
from queue import Queue, Empty
import sqlite3 as sq
from typing import Type
from sqliterequests import Table, Select, Insert, Where
from time import sleep

class KeyCharacter:
    id: int  
    guid: int
    name: str
    spec_id: int
    ilvl: int
    covenant_id: int
    soulbind_id: int
    ID = 'id'
    GUID = 'guid'
    NAME = 'name'
    SPEC_ID = 'specID'
    ILVL = 'Ilvl'
    COVENANT_ID = 'CovenantID'
    SOULBIND_ID = 'SoulbindID'
    ARGS = [ID, GUID, NAME, SPEC_ID, ILVL, COVENANT_ID, SOULBIND_ID]

    def __str__(self):
        s = [self.id, self.guid, self.name, self.spec_id, self.ilvl, self.covenant_id, self.soulbind_id]
        str = ''
        for i in range(len(s)):
            str += f"{self.ARGS[i]} = {s[i]}; "
        return str

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
    ARGS = [ID, INST, AFFIXES, CHALLENGE_LEVEL, DATE, RECORD_TIME, TIMER_LEVEL]

    def __str__(self):
        s = [self.id, self.inst, self.affixes, self.challenge_level, self.date, self.record_time, self.timer_level]
        str = ''
        for i in range(len(s)):
            str += f"{self.ARGS[i]} = {s[i]}; "
        return str

class Character:
    guid: int
    name: str
    keys: str
    GUID = 'guid' 
    NAME = 'name'
    KEYS = 'keys'
    ARGS = [GUID, NAME, KEYS]

    def __str__(self):
        s = [self.guid, self.name, self.keys]
        str = ''
        for i in range(len(s)):
            str += f"{self.ARGS[i]} = {s[i]}; "
        return str


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

class MythicDataBase:
    MYTHIC = Table('mythic')
    MYTHIC_GUID = Table('mythic_guid')
    CHARACTERS = Table('characters')

    def __init__(self) -> None:
        self.conn = sq.connect('data.db')
        self.cur = self.conn.cursor()
        self._size = self.cur.execute(f'SELECT COUNT(*) FROM {MythicDataBase.MYTHIC.name}').fetchone()[0]

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
            Insert(
                self.MYTHIC, 
                Key.ARGS,
                [key.id, key.inst, key.affixes, key.challenge_level, key.date, key.record_time, key.timer_level]
            ).get()
        ).lastrowid
        for member in key.characters:
            self.cur.execute(
                Insert(
                    self.MYTHIC_GUID, 
                    KeyCharacter.ARGS,
                    [member.id, member.guid, member.name, member.spec_id, member.ilvl, member.covenant_id, member.soulbind_id]
                ).get()
            )
            keys = self.cur.execute(
                Where(Select(self.CHARACTERS, [Character.KEYS]), [Character.GUID], [member.guid]).get()
            ).fetchone()
            if keys:
                self.cur.execute(
                    f'''UPDATE characters SET {Character.KEYS} = '{keys[0]+' '+str(id)}' WHERE {Character.guid}={member.guid}'''
                )
            else:
                self.cur.execute(
                    Insert(
                        self.CHARACTERS,
                        Character.ARGS,
                        [member.guid, member.name, id]
                    ).get()
                )
        self.size+=1

    def get_character_by_name(self, name: str) -> list[Type[Character]]:
        '''SELECT character whose nickname start with name'''
        res = self.cur.execute(
            Select(
                self.CHARACTERS,
                Character.ARGS
            ).get() + 
            f''' WHERE {Character.NAME} LIKE '{name}%' '''
        )
        chars = []
        for i in res.fetchall():
            char = Character()
            char.guid = i[0]
            char.name = i[1]
            char.keys = i[2]
            chars.append(char)
        return chars

    def get_character_by_guid(self, guid: int) -> Type[Character]:
        '''SELECT character whose nickname start with name'''
        res = self.cur.execute(
            Where(
                Select(
                    self.CHARACTERS,
                    Character.ARGS
                ),
                [Character.GUID],
                [guid]
            ).get()
        )
        i = res.fetchone()
        char = Character()
        char.guid = i[0]
        char.name = i[1]
        char.keys = i[2]
        return char

    def get_character_by_key_id(self, id: int) -> list[Type[KeyCharacter]]:
        '''SELECT characters from key by key id'''
        res = self.cur.execute(
            Where(Select(self.MYTHIC_GUID, [], True), [KeyCharacter.ID], [id]).get()
        )
        chars = []
        for i in res.fetchall():
            char = KeyCharacter()
            char.id = i[0]
            char.guid = i[1]
            char.name = i[2]
            char.spec_id = i[3]
            char.ilvl = i[4]
            char.covenant_id = i[5]
            char.soulbind_id = i[6]
            chars.append(char)
        return chars

    def get_keys(self, offset: int = 0, limit: int = 10) -> list[Type[Key]]:
        '''SELECT limit keys wit offset'''
        res = self.cur.execute(
            Select(self.MYTHIC, [], True).get() + f''' LIMIT {offset}, {limit}'''
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

    def get_character_keys(self, name: str = None, guid: int = None):
        if guid:
            cmd = Where(Select(self.CHARACTERS, [Character.KEYS]), [Character.GUID], [guid]).get()
        if name:
            cmd = Where(Select(self.CHARACTERS, [Character.KEYS]), [Character.NAME], [name]).get()
        res = self.cur.execute(cmd).fetchone()[0].split()
        keys = []
        for i in res:
            keys.append(self.get_keys(int(i)-1)[0])
        return keys
    
    def size(self) -> int:
        return self._size
class AsyncMythicDataBase:
    queue: Queue
    MDB: MythicDataBase
    MYTHIC = Table('mythic')
    MYTHIC_GUID = Table('mythic_guid')
    CHARACTERS = Table('characters')

    class Result:
        result = None

        def put(self, result):
            self.result = result

        def get(self):
            while not self.result:
                pass
            return self.result

    def __init__(self) -> None:
        def init(queue: Queue):
            self.MDB = MythicDataBase()
            while True:
                try:
                    req = queue.get()
                except Empty:
                    continue
                else:
                    req[2].put(req[0](*req[1]))
                    queue.task_done()
        self.queue = Queue()
        Thread(target = init, args = (self.queue,), daemon = True).start()
        sleep(1)

    def add_key(self, key: Key) -> None:
        self.queue.put((self.MDB.add_key, (key,)))

    def get_keys(self, offset: int = 0, limit: int = 10) -> list[Key]:
        '''SELECT limit keys wit offset'''
        res = self.Result()
        self.queue.put((self.MDB.get_keys, (offset, limit), res))
        return res
    
    def size(self) -> int:
        res = self.Result()
        self.queue.put((self.MDB.size, (), res))
        return res

MDB = AsyncMythicDataBase()

if __name__ == '__main__':
    print('MAIN():')