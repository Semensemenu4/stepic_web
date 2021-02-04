import requests
from collections import Counter
import datetime

now = datetime.datetime.now()
curent_year = now.year


def get_id_user( username,  token, proxies ):
    url = 'https://api.vk.com/method/users.get?v=5.71&access_token=' + token + '&user_ids=' + str( username )
    r = requests.get(url, proxies=proxies)
    id = r.json()

    return id['response'][0]['id']


def get_friends_list( id, token, proxies ):
    url = 'https://api.vk.com/method/friends.get?v=5.71&access_token=' + token + '&user_id=' + str(id) + '&fields=bdate'
    r = requests.get(url, proxies=proxies)
    fr = r.json()

    return fr['response']['items']


def calc_age( uid ):
    TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'
    proxies = {
        'https' : "51.158.107.202:9999"
    }

    # получаем айди
    id = get_id_user( uid, TOKEN, proxies )
    print(id)

    #получаем список всех друзей
    friends = get_friends_list( id, TOKEN, proxies )

    # убираем всех без даты и без указания года рождения, получаем только возраст
    only_age = [ i for i in friends if i.get('bdate') ]
    only_year = [ i['bdate'].split('.') for i in only_age if len(i['bdate'].split('.')) > 2 ]
    list_of_ages = [ curent_year - int( i[2] ) for i in only_year ]

    #сортируем список с возрастом
    sorted_list = dict( Counter( list_of_ages ) )
    print(sorted_list)

    final = []
    def sorted_key(val):
        return val[1]

    for k, v in sorted(sorted_list.items(), key=sorted_key, reverse=True):
        final.append( (k, sorted_list[k]) )


    return sorted(final, key=lambda x: ( -x[1], x[0] ) )


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
