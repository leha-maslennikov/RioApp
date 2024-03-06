import requests
from mythicdatabase import Key, KeyCharacter, AsyncMythicDataBase
from secret import login, password
import wow
import datetime
from time import sleep, time

json_data = [
    {
        'tid': 12,
        'data': [
            {
                'page': 1,
                'start': 0,
                'limit': 25,
                'sort': [
                    {
                        'property': None,
                        'direction': 'ASC',
                    },
                ],
                'filter': [],
            },
        ],
        'action': 'wow_Services',
        'type': 'rpc',
        'method': 'cmdGetChallenge',
    },
]

def get_page():
    t = time()
    while True:
        response = ses.post('https://cpsl.wowcircle.me/main.php?1&serverId=null', json=json_data)
        if response.status_code != 200:
            print('get_page_1: ', response.status_code)
            print('get_page_1: ', response.text)
            exit(0)
        if json_data[0]['data'][0]['page'] % 100 == 0:
            print(json_data[0]['data'][0]['page'], time()-t)
            t = time()
        json_data[0]['data'][0]['page'] += 1
        json_data[0]['data'][0]['start'] += 25
        #json_data[0]['tid']+=1
        try:
            #print(json_data[0]['data'][0]['page'])
            yield response.json()
        except Exception as e:
            print('get_page_2: ', e)
            print('get_page_2: ', response.status_code)
            print('get_page_2: ', response.text)


def parse():
    for js in get_page():
        try:
            for row_key in js['result']['data']:
                key = Key()
                key.id = None
                key.inst = wow.dung[row_key['MapID']]
                key.affixes = ' '.join([wow.get_affix_img(i) for i in row_key['Affixes'].split()])
                key.challenge_level = int(row_key['ChallengeLevel'])
                key.date = str(datetime.datetime.utcfromtimestamp(int(row_key['Date'])))
                key.record_time = str(datetime.timedelta(seconds=int(row_key['RecordTime'])))
                key.timer_level = int(row_key['TimerLevel'])
                key.score = wow.get_score(key.challenge_level, key.timer_level)
                key.characters = []
                for row_member in row_key['members']:
                    memeber = KeyCharacter()
                    memeber.id = None
                    memeber.guid = int(row_member['guid'])
                    memeber.name = row_member['name']
                    memeber.spec_id = int(row_member['specID'])
                    memeber.ilvl = int(row_member['Ilvl'])
                    memeber.covenant_id = int(row_member['CovenantID'])
                    memeber.soulbind_id = int(row_member['SoulbindID'])
                    memeber.inst = key.inst
                    memeber.score = key.score
                    memeber.affixes = key.affixes
                    key.characters.append(memeber)
                MDB.add_key(key)
        except Exception as e:
            print("parse_exception: ", e)
            print('end of list')
            break
            exit(0)


def get_all_keys(ses: requests.Session):
    ses.get(url='https://cpsl.wowcircle.me')
    ses.post(url='https://cpsl.wowcircle.me/main.php?1&serverId=null', data='[{"tid":4,"data":[{"accountName":"'+login+'","password":"'+password+'","captcha":""}],"action":"wow_Services","type":"rpc","method":"cmdLogin"}]')
    MDB.create().get()
    parse()

if __name__ == '__main__':
    MDB = AsyncMythicDataBase('data.db', 1)
    ses = requests.session()
    get_all_keys(ses)
    ses.close()
    print('----------1')
    MDB.flush().get()
    print('----------2')
    MDB.count_score()
    print('----------3')