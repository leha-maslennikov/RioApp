from threading import Thread
from queue import Queue, Empty
import sqlite3 as sq
from sqliterequests import *
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
    score: int
    characters: list[KeyCharacter]
    ID = 'id'
    INST = 'inst'
    AFFIXES = 'Affixes'
    CHALLENGE_LEVEL = 'ChallengeLevel'
    DATE = 'Date'
    RECORD_TIME = 'RecordTime'
    TIMER_LEVEL = 'TimerLevel'
    SCORE = 'score'
    ARGS = [ID, INST, AFFIXES, CHALLENGE_LEVEL, DATE, RECORD_TIME, TIMER_LEVEL, SCORE]

    def __str__(self):
        s = [self.id, self.inst, self.affixes, self.challenge_level, self.date, self.record_time, self.timer_level, self.score]
        str = ''
        for i in range(len(s)):
            str += f"{self.ARGS[i]} = {s[i]}; "
        return str

class Character:
    guid: int
    name: str
    keys: str
    score: int
    tank_score: int
    heal_score: int
    dps_score: int
    GUID = 'guid' 
    NAME = 'name'
    KEYS = 'keys'
    SCORE = 'score'
    TANK_SCORE = 'tank_score'
    HEAL_SCORE = 'heal_score'
    DPS_SCORE = 'dps_score'
    ARGS = [GUID, NAME, KEYS, SCORE, TANK_SCORE, HEAL_SCORE, DPS_SCORE]

    def __str__(self):
        s = [self.guid, self.name, self.keys, self.score, self.tank_score, self.heal_score, self.dps_score]
        str = ''
        for i in range(len(s)):
            str += f"{self.ARGS[i]} = {s[i]}; "
        return str

class MythicDataBase:
    MYTHIC = Table('mythic')
    MYTHIC_GUID = Table('mythic_guid')
    CHARACTERS = Table('characters')

    def __init__(self) -> None:
        self.conn = sq.connect('data.db')
        self.cur = self.conn.cursor()
        try:
            self._size = self.cur.execute(f'SELECT COUNT(*) FROM {MythicDataBase.MYTHIC.name}').fetchone()[0]
        except:
            self._size = 0
    
    def __del__(self) -> None:
        self.cur.close()
        self.conn.close()

    def create(self):
        '''
        DROP IF EXIST AND CREATE mythic, characters, mythic_guid
        Affixes ChallengeLevel Date RecordTime TimerLevel
        guid name specID CovenantID SoulbindID'''
        self.cur.execute(f'DROP TABLE IF EXISTS {self.MYTHIC.name}')
        self.cur.execute(f'DROP TABLE IF EXISTS {self.CHARACTERS.name}')
        self.cur.execute(f'DROP TABLE IF EXISTS {self.MYTHIC_GUID.name}')
        self.cur.execute(
            f'''
            CREATE TABLE mythic (
                {Key.ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                {Key.INST} TEXT,
                {Key.AFFIXES} TEXT,
                {Key.CHALLENGE_LEVEL} INTEGER,
                {Key.DATE} TEXT,
                {Key.RECORD_TIME} TEXT,
                {Key.TIMER_LEVEL} INTEGER,
                {Key.SCORE} INTEGER
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
                {Character.KEYS} TEXT,
                {Character.SCORE} INTEGER,
                {Character.TANK_SCORE} INTEGER,
                {Character.HEAL_SCORE} INTEGER,
                {Character.DPS_SCORE} INTEGER
            )'''
        )

    def add_key(self, key: Key) -> None:
        '''add key to MYTHIC table'''
        id = self.cur.execute(
            Insert(
                self.MYTHIC, 
                Key.ARGS[1:],
                [key.inst, key.affixes, key.challenge_level, key.date, key.record_time, key.timer_level, key.score]
            ).get()
        ).lastrowid
        for member in key.characters:
            self.cur.execute(
                Insert(
                    self.MYTHIC_GUID, 
                    KeyCharacter.ARGS,
                    [id, member.guid, member.name, member.spec_id, member.ilvl, member.covenant_id, member.soulbind_id]
                ).get()
            )
            keys = self.cur.execute(
                Where(Select(self.CHARACTERS, [Character.KEYS]), [Character.GUID], [member.guid]).get()
            ).fetchone()
            if keys:
                self.cur.execute(
                    Where(Update(self.CHARACTERS, [Character.KEYS], [keys[0]+' '+str(id)]), [Character.GUID], [member.guid]).get()
                )
            else:
                self.cur.execute(
                    Insert(
                        self.CHARACTERS,
                        Character.ARGS,
                        [member.guid, member.name, str(id), 0, 0, 0, 0]
                    ).get()
                )
        self._size+=1

    def count_score(self, offset: int, limit: int):
        res = self.cur.execute(
            Select(self.CHARACTERS, [], all=True).get() + f''' LIMIT {offset}, {limit}'''
        )

    def get_character_by_name(self, name: str) -> list[Character]:
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
            char.score = i[3]
            char.tank_score = i[4]
            char.heal_score = i[5]
            char.dps_score = i[6]
            chars.append(char)
        return chars

    def get_character_by_guid(self, guid: int) -> Character:
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
        char.score = i[3]
        char.tank_score = i[4]
        char.heal_score = i[5]
        char.dps_score = i[6]

        return char

    def get_characters_by_key_id(self, id: int) -> list[KeyCharacter]:
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

    def get_keys(self, offset: int = 0, limit: int = 10, column: list[str] = [Key.ID], reverse: list[bool] = [False]) -> list[Key]:
        '''SELECT limit keys with offset Sorted by column with [reverse] order'''
        res = self.cur.execute(
            Order(
                Select(self.MYTHIC, [], True),
                column,
                reverse
            ).get() + f''' LIMIT {offset}, {limit}'''
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
            key.score = i[7]
            keys.append(key)
        return keys

    def get_character_keys(self, name: str = None, guid: int = None) -> list[Key]:
        '''return character keys by character's name or guid'''
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
    
    def flush(self) -> None:
        self.conn.commit()

class AsyncMythicDataBase:
    queue: Queue
    MDB: MythicDataBase
    MYTHIC = Table('mythic')
    MYTHIC_GUID = Table('mythic_guid')
    CHARACTERS = Table('characters')

    class Result:
        have_result = False
        result = None

        def put(self, result):
            self.have_result = True
            self.result = result

        def get(self):
            while not self.have_result:
                pass
            return self.result

    def __init__(self) -> None:
        def handler(queue: Queue):
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
        Thread(target = handler, args = (self.queue,), daemon = True).start()
        sleep(1)

    def flush(self) -> Result:
        res = self.Result()
        self.queue.put((self.MDB.flush, (), res))
        return res

    def create(self) -> Result:
        '''DROP IF EXIST AND CREATE mythic, characters, mythic_guid
        Affixes ChallengeLevel Date RecordTime TimerLevel
        guid name specID CovenantID SoulbindID'''
        res = self.Result()
        self.queue.put((self.MDB.create, (), res))
        return res

    def add_key(self, key: Key) -> Result:
        '''add key to MYTHIC table'''
        res = self.Result()
        self.queue.put((self.MDB.add_key, (key,), res))
        return res

    def get_character_by_name(self, name: str) -> list[Character]:
        '''SELECT character whose nickname start with name'''
        res = self.Result()
        self.queue.put((self.MDB.get_character_by_name, (name,), res))
        return res

    def get_character_by_guid(self, guid: int) -> Character:
        '''SELECT character whose nickname start with name'''
        res = self.Result()
        self.queue.put((self.MDB.get_character_by_guid, (guid), res))
        return res

    def get_characters_by_key_id(self, id: int) -> list[KeyCharacter]:
        '''SELECT characters from key by key id'''
        res = self.Result()
        self.queue.put((self.MDB.get_characters_by_key_id, (id,), res))
        return res

    def get_keys(self, offset: int = 0, limit: int = 10, column: list[str] = [Key.ID], reverse: list[bool] = [False]) -> list[Key]:
        '''SELECT limit keys wit offset'''
        res = self.Result()
        self.queue.put((self.MDB.get_keys, (offset, limit, column, reverse), res))
        return res

    def get_character_keys(self, name: str = None, guid: int = None) -> list[Key]:
        '''return character keys by character's name or guid'''
        res = self.Result()
        self.queue.put((self.MDB.get_character_keys, (name, guid), res))
        return res
      
    def size(self) -> int:
        res = self.Result()
        self.queue.put((self.MDB.size, (), res))
        return res

MDB = AsyncMythicDataBase()

if __name__ == '__main__':
    print('MAIN():')
    #print(' '.join(map(str, MDB.get_keys(0, column=[Key.Da]).get())))
    sleep(3)