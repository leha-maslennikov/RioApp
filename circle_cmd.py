import requests
import db
from secret import login, password

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
            print('get_page_1: ',response.text)
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
            for key in js['result']['data']:
                db.add_key(key)
        except Exception as e:
            print("parse_exception: ", e)
            print(js)
            exit(0)


def get_all_keys():
    ses.get(url='https://cpsl.wowcircle.me')
    ses.post(url='https://cpsl.wowcircle.me/main.php?1&serverId=null', data='[{"tid":4,"data":[{"accountName":"'+login+'","password":"'+password+'","captcha":""}],"action":"wow_Services","type":"rpc","method":"cmdLogin"}]')
    db.create()
    parse()


if __name__ == '__main__':
    ses = requests.session()
    get_all_keys()