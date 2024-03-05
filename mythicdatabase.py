from threading import Thread
#from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
import sqlite3 as sq
from sqliterequests import *
from time import sleep, time

class KeyCharacter:
    id: int  
    guid: int
    name: str
    spec_id: int
    ilvl: int
    covenant_id: int
    soulbind_id: int
    inst: str
    score: int
    affixes: str
    ID = 'id'
    GUID = 'guid'
    NAME = 'name'
    SPEC_ID = 'specID'
    ILVL = 'Ilvl'
    COVENANT_ID = 'CovenantID'
    SOULBIND_ID = 'SoulbindID'
    INST = 'inst'
    SCORE = 'score'
    AFFIXES = 'affixes'
    ARGS = [ID, GUID, NAME, SPEC_ID, ILVL, COVENANT_ID, SOULBIND_ID, INST, SCORE, AFFIXES]

    def __str__(self):
        s = [self.id, self.guid, self.name, self.spec_id, self.ilvl, self.covenant_id, self.soulbind_id, self.inst, self.score]
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
class AsyncMythicDataBase:
    queue: Queue
    name: str
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

    def __init__(self, name: str, number_of_threads: int) -> None:
        def handler(queue: Queue):
            while True:
                try:
                    req = queue.get()
                except Empty:
                    continue
                else:
                    while True:
                        try:
                            with sq.connect(self.name) as conn:
                                req(conn)
                            queue.task_done()
                        except Exception as er:
                            print(er)
                            continue
                        break
        self.queue = Queue()
        self.name = name
        for i in range(number_of_threads):
            Thread(target = handler, args = (self.queue,), daemon = True).start()
        with sq.connect(self.name) as conn:
            try:
                self._size = conn.execute(f'SELECT COUNT(*) FROM {self.MYTHIC.name}').fetchone()[0]
            except:
                self._size = 0

    def flush(self) -> Result:
        res = self.Result()
        def f(conn: sq.Connection):
            conn.commit()
            res.put(True)
        self.queue.put(f)
        return res

    def create(self) -> None:
        '''DROP IF EXIST AND CREATE mythic, characters, mythic_guid
        Affixes ChallengeLevel Date RecordTime TimerLevel
        guid name specID CovenantID SoulbindID'''
        res = self.Result()
        def f(conn: sq.Connection):
            conn.execute(f'DROP TABLE IF EXISTS {self.MYTHIC.name}')
            conn.execute(f'DROP TABLE IF EXISTS {self.CHARACTERS.name}')
            conn.execute(f'DROP TABLE IF EXISTS {self.MYTHIC_GUID.name}')
            conn.execute(
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
            conn.execute(
                f'''
                CREATE TABLE mythic_guid (
                    {KeyCharacter.ID} INTEGER,  
                    {KeyCharacter.GUID} INTEGER,
                    {KeyCharacter.NAME} TEXT,
                    {KeyCharacter.SPEC_ID} INTEGER,
                    {KeyCharacter.ILVL} INTEGER,
                    {KeyCharacter.COVENANT_ID} INTEGER, 
                    {KeyCharacter.SOULBIND_ID} INTEGER,
                    {KeyCharacter.INST} TEXT,
                    {KeyCharacter.SCORE} INTEGER,
                    {KeyCharacter.AFFIXES} TEXT
                )'''
            )
            conn.execute(
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
            res.put(True)
        self.queue.put(f)
        return res

    def add_key(self, key: Key) -> Result:
        '''add key to MYTHIC table'''
        res = self.Result()
        def f(conn: sq.Connection):
            id = conn.execute(
                Insert(
                    self.MYTHIC, 
                    Key.ARGS[1:],
                    [key.inst, key.affixes, key.challenge_level, key.date, key.record_time, key.timer_level, key.score]
                ).get()
            ).lastrowid
            for member in key.characters:
                conn.execute(
                    Insert(
                        self.MYTHIC_GUID, 
                        KeyCharacter.ARGS,
                        [id, member.guid, member.name, member.spec_id, member.ilvl, member.covenant_id, member.soulbind_id, member.inst, member.score, member.affixes]
                    ).get()
                )
                keys = conn.execute(
                    Where(Select(self.CHARACTERS, [Character.KEYS]), [Character.GUID], [member.guid]).get()
                ).fetchone()
                if keys:
                    conn.execute(
                        Where(Update(self.CHARACTERS, [Character.KEYS], [keys[0]+' '+str(id)]), [Character.GUID], [member.guid]).get()
                    )
                else:
                    conn.execute(
                        Insert(
                            self.CHARACTERS,
                            Character.ARGS,
                            [member.guid, member.name, str(id), 0, 0, 0, 0]
                        ).get()
                    )
            self._size+=1
            res.put(True)
        self.queue.put(f)
        return res

    def exe(self, req: Request) -> Result:
        res = self.Result()
        def f(conn: sq.Connection):
            res.put(conn.execute(req.get()).fetchall())
        self.queue.put(f)
        return res

    def get_characters(self, offset: int = 0, limit: int = 10, column: list[str] = [Character.NAME], reverse: list[bool] = [False]) -> list[Character]:
        '''SELECT limit characters with offset Sorted by column with [reverse] order'''
        res = self.Result()
        def f(conn: sq.Connection):
            r = conn.execute(
                Order(
                    Select(self.CHARACTERS, [], True),
                    column,
                    reverse
                ).get() + f''' LIMIT {offset}, {limit}'''
            )
            chars = []
            for i in r.fetchall():
                char = Character()
                char.guid = int(i[0])
                char.name = i[1]
                char.keys = i[2]
                char.score = int(i[3])
                char.tank_score = int(i[4])
                char.heal_score = int(i[5])
                char.dps_score = int(i[6])
                chars.append(char)
            res.put(chars)
        self.queue.put(f)
        return res

    def count_score(self):
        import wow
        #with ThreadPoolExecutor(1) as exe:
        offset = 0
        limit = 10
        t = time()
        k = 1
        with sq.connect(self.name) as conn:
            while True:
                r = conn.execute(
                    Order(
                        Select(self.CHARACTERS, [], True),
                        [Character.NAME],
                        [False]
                    ).get() + f''' LIMIT {offset}, {limit}'''
                )
                chars = []
                for i in r.fetchall():
                    char = Character()
                    char.guid = int(i[0])
                    char.name = i[1]
                    char.keys = i[2]
                    char.score = int(i[3])
                    char.tank_score = int(i[4])
                    char.heal_score = int(i[5])
                    char.dps_score = int(i[6])
                    chars.append(char)
                offset+=limit
                if not chars:
                    break
                for char in chars:
                    res = conn.execute(
                        Where(
                            Select(self.MYTHIC_GUID, [KeyCharacter.SPEC_ID, KeyCharacter.INST, KeyCharacter.SCORE, KeyCharacter.AFFIXES]),
                            [KeyCharacter.GUID],
                            [char.guid]
                        ).get()
                    ).fetchall()
                    wow.count_score(char, res)
                    conn.execute(
                        Where(
                            Update(
                                self.CHARACTERS,
                                [Character.SCORE, Character.TANK_SCORE, Character.HEAL_SCORE, Character.DPS_SCORE],
                                [char.score, char.tank_score, char.heal_score, char.dps_score]
                            ),
                            [Character.GUID],
                            [char.guid]
                        ).get()
                    )
                if offset // 100 == k:
                    conn.commit()
                    k+=1
                    print(offset, time()-t)
                    t = time()
                

    def get_character_by_name(self, name: str) -> list[Character]:
        '''SELECT character whose nickname start with name'''
        res = self.Result()
        def f(conn: sq.Connection):
            r = conn.execute(
                Select(
                    self.CHARACTERS,
                    Character.ARGS
                ).get() + 
                f''' WHERE {Character.NAME} LIKE '{name}%' '''
            )
            chars = []
            for i in r.fetchall():
                char = Character()
                char.guid = i[0]
                char.name = i[1]
                char.keys = i[2]
                char.score = i[3]
                char.tank_score = i[4]
                char.heal_score = i[5]
                char.dps_score = i[6]
                chars.append(char)
            res.put(chars)
        self.queue.put(f)
        return res

    def get_character_by_guid(self, guid: int) -> Character:
        '''SELECT character by guid'''
        res = self.Result()
        def f(conn: sq.Connection):
            r = conn.execute(
                Where(
                    Select(
                        self.CHARACTERS,
                        Character.ARGS
                    ),
                    [Character.GUID],
                    [guid]
                ).get()
            )
            i = r.fetchone()
            char = Character()
            char.guid = i[0]
            char.name = i[1]
            char.keys = i[2]
            char.score = i[3]
            char.tank_score = i[4]
            char.heal_score = i[5]
            char.dps_score = i[6]
            res.put(char)
        self.queue.put(f)
        return res

    def get_characters_by_key_id(self, id: int) -> list[KeyCharacter]:
        '''SELECT characters from key by key id'''
        res = self.Result()
        def f(conn: sq.Connection):
            r = conn.execute(
                Where(Select(self.MYTHIC_GUID, [], True), [KeyCharacter.ID], [id]).get()
            ).fetchall()
            chars = []
            for i in r:
                char = KeyCharacter()
                char.id = i[0]
                char.guid = i[1]
                char.name = i[2]
                char.spec_id = i[3]
                char.ilvl = i[4]
                char.covenant_id = i[5]
                char.soulbind_id = i[6]
                char.inst = i[7]
                char.score = i[8]
                char.affixes = i[9]
                chars.append(char)
            res.put(chars)
        self.queue.put(f)
        return res

    def get_keys(self, offset: int = 0, limit: int = 10, column: list[str] = [Key.ID], reverse: list[bool] = [False]) -> list[Key]:
        '''SELECT limit keys wit offset'''
        res = self.Result()
        def f(conn: sq.Connection):
            r = conn.execute(
                Order(
                    Select(self.MYTHIC, [], True),
                    column,
                    reverse
                ).get() + f''' LIMIT {offset}, {limit}'''
            ).fetchall()
            keys = []
            chars = [self.get_characters_by_key_id(i[0]) for i in r]
            for i in range(len(r)):
                key = Key()
                key.id = r[i][0]
                key.inst = r[i][1]
                key.affixes = r[i][2]
                key.challenge_level = r[i][3]
                key.date = r[i][4]
                key.record_time = r[i][5]
                key.timer_level = r[i][6]
                key.score = r[i][7]
                key.characters = chars[i]
                keys.append(key)
            res.put(keys)
        self.queue.put(f)
        return res

    def get_key_by_id(self, id: int) -> Key:
        res = self.Result()
        def f(conn: sq.Connection):
            i = conn.execute(
                Where(
                    Select(self.MYTHIC, [], True),
                    [Key.ID],
                    [id]
                ).get()
            ).fetchone()
            key = Key()
            key.id = i[0]
            key.inst = i[1]
            key.affixes = i[2]
            key.challenge_level = i[3]
            key.date = i[4]
            key.record_time = i[5]
            key.timer_level = i[6]
            key.score = i[7]
            key.characters = self.get_characters_by_key_id(key.id)
            res.put(key)
        self.queue.put(f)
        return res

    def get_character_keys(self, name: str = None, guid: int = None) -> list[Key]:
        '''return character keys by character's name or guid'''
        res = self.Result()
        def f(conn: sq.Connection):
            if guid:
                cmd = Where(Select(self.CHARACTERS, [Character.KEYS]), [Character.GUID], [guid]).get()
            if name:
                cmd = Where(Select(self.CHARACTERS, [Character.KEYS]), [Character.NAME], [name]).get()
            r = conn.execute(cmd).fetchone()[0].split()
            keys = []
            for i in r:
                keys.append(self.get_key_by_id(int(i)))
            res.put(keys)
        self.queue.put(f)
        return res
      
    def size(self) -> int:
        return self._size

MDB = AsyncMythicDataBase('data.db', 2)

if __name__ == '__main__':
    print('MAIN():', MDB)
    #MDB.count_score()
    MDB.flush().get()
    