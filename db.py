import sqlite3 as sq
import datetime

#print(datetime.datetime.utcfromtimestamp(1705693235))
#print(datetime.timedelta(seconds=2147))


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

def create():
    '''
    DROP IF EXIST AND CREATE mythic, characters, mythic_guid
    Affixes ChallengeLevel Date RecordTime TimerLevel
    guid name specID CovenantID SoulbindID'''
    with sq.connect('data.db') as conn:
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS mythic')
        cur.execute('DROP TABLE IF EXISTS characters')
        cur.execute('DROP TABLE IF EXISTS mythic_guid')
        cur.execute(
            '''
            CREATE TABLE mythic (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inst TEXT,
                Affixes TEXT,
                ChallengeLevel INTEGER,
                Date TEXT,
                RecordTime TEXT,
                TimerLevel INTEGER
            )'''
        )
        cur.execute(
            '''
            CREATE TABLE mythic_guid (
                id INTEGER,  
                guid INTEGER,
                name TEXT,
                specID INTEGER,
                Ilvl INTEGER,
                CovenantID INTEGER, 
                SoulbindID INTEGER
            )'''
        )
        cur.execute(
            '''
            CREATE TABLE characters (
                guid INTEGER PRIMARY KEY,  
                name TEXT,
                keys TEXT
            )'''
        )

def add_key(key: dict):
    '''key json added in db'''
    with sq.connect('data.db') as conn:
        cur = conn.cursor()
        id = cur.execute(
            f'''
            INSERT INTO mythic(inst, Affixes, ChallengeLevel, Date, RecordTime, TimerLevel) VALUES
            ('{dung[key['MapID']]}', '{key['Affixes']}', {key['ChallengeLevel']}, '{datetime.datetime.utcfromtimestamp(int(key['Date']))}', '{datetime.timedelta(seconds=int(key['RecordTime']))}', {key['TimerLevel']})
            '''
        ).lastrowid
        for member in key['members']:
            cmd = f'''
                INSERT INTO mythic_guid(id, guid, name, specID, Ilvl, CovenantID, SoulbindID) VALUES
                ({id}, {member['guid']}, '{member['name']}', {member['specID']}, {member['Ilvl']}, {member['CovenantID']}, {member['SoulbindID']})
                    '''
            cur.execute(cmd)
            keys = cur.execute(f"SELECT keys FROM characters WHERE guid={member['guid']}").fetchone()
            if keys:
                cur.execute(
                    f'''UPDATE characters SET keys = '{keys[0]+' '+str(id)}' WHERE guid={member['guid']}'''
                )
            else:
                cur.execute(
                    f'''INSERT INTO characters(guid, name, keys) VALUES ({member['guid']}, '{member['name']}', '{id}')'''
                )



def get_character_by_name(name):
    '''SELECT character whose nickname start with name'''
    with sq.connect('data.db') as conn:
        cur = conn.cursor()
        res = cur.execute(
            f'''SELECT guid, name FROM characters WHERE name LIKE '{name}%' '''
        )
        return res.fetchall() 
      

def get_keys(limit, offset):
    '''SELECT limit keys wit offset'''
    with sq.connect('data.db') as conn:
        cur = conn.cursor()
        res = cur.execute(
            f'''SELECT * FROM mythic LIMIT {offset}, {limit} '''
        )
        return res.fetchall() 
    

def get_character_by_key(id):
    '''SELECT characters from key with id'''
    with sq.connect('data.db') as conn:
        cur = conn.cursor()
        res = cur.execute(
            f'''SELECT * FROM mythic_guid WHERE id = {id}'''
        )
        return res.fetchall() 
print(get_character_by_key(1))