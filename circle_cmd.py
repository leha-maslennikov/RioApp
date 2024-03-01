import requests
from mythicdatabase import MDB, Key, KeyCharacter
from secret import login, password
import wow
import datetime

json_data = [
    {
        'tid': 13,
        'data': [
            {
                'page': 0,
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
    while True:
        response = ses.post('https://cpsl.wowcircle.me/main.php?1&serverId=null', json=json_data)
        if response.status_code != 200:
            print('get_page_1: ', response.status_code)
            print('get_page_1: ', response.text)
            exit(0)
        if json_data[0]['data'][0]['page'] % 100 == 0:
            print(json_data[0]['data'][0]['page'])
        json_data[0]['data'][0]['page'] += 1
        json_data[0]['data'][0]['start'] += 25
        try:
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
                    key.characters.append(memeber)
                MDB.add_key(key)
                MDB.flush()
        except Exception as e:
            print("parse_exception: ", e)
            print(js)
            break
            exit(0)
        break


def get_all_keys():
    ses.get(url='https://cpsl.wowcircle.me')
    ses.post(url='https://cpsl.wowcircle.me/main.php?1&serverId=null', data='[{"tid":4,"data":[{"accountName":"'+login+'","password":"'+password+'","captcha":""}],"action":"wow_Services","type":"rpc","method":"cmdLogin"}]')
    MDB.create().get()

    parse()


if __name__ == '__main__':
    ses = requests.session()
    get_all_keys()