import pymongo
import math
import matplotlib.pyplot as plt
from hero_dictionary import hero_dic
import matplotlib.dates as mdates
conn = pymongo.MongoClient()
db = conn['dota-db']


def hero_per_month(player_id, hero_id):
    match_search_args = {
                'result.game_mode': {'$in': [0, 1, 2, 3, 4, 5, 12, 14, 16, 22]},
                'result.duration': {'$gt': 720},
                'result.players.level': {'$nin': [1, 2, 3]},
                'result.players.leaver_status': {'$nin': [5, 6]},
                'result.lobby_type': {'$in': [0, 5, 6, 7]}
                }

    custom_args = {
                'result.players.account_id': player_id}
    custom_args.update(match_search_args)
    cursor = db['{}'.format(player_id)].find(custom_args)
    cursor.sort('result.start_time', 1)
    hist = list(cursor)
    time = hist[0]['result']['start_time']

    quantity = []
    kk = 0
    m = 0
    q = 0
    month = []
    for i in hist:

        if i['result']['start_time'] < time:
            for j in range(10):
                try:
                    if i['result']['players'][j]['account_id'] == player_id:

                        if i['result']['players'][j]['hero_id'] == hero_id:
                            q += 1
                            kk += 1
                except:
                        pass
        else:
            time += 2592000
            quantity.append(q)
            month.append(time)
            q = 0
            m += 1

    plt.xkcd()
    plt.gca().cla()

    plt.title('number of games played as {} per month'.format(hero_dic[hero_id]))

    y = quantity

    secs = mdates.epoch2num(month)

    ax = plt.gca()

    years = mdates.YearLocator()   # every year
    yearsFmt = mdates.DateFormatter('%Y')

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    tick = 5 if max(y) > 20 else 1
    #yint = range(min(y), math.ceil(max(y))+2, tick)  # set only int ticks
    #plt.yticks(yint)
    plt.plot(secs, y, color='blue')

    plt.savefig('images/graphs/hero.png')

    return "{} games".format(kk)

hero_per_month(56232406, 6)