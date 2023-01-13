import os
import sys
import time
import redis
import re
from datetime import datetime
import pytz

time_epoch_unit = 5 * 60 # 5 min
tz = pytz.timezone('Asia/Taipei')

redis_client = redis.Redis('localhost', 6379, 0)

# TODO 一小時關鍵字次數(每次計算)

'''
過去 24小時出現的{實體}關鍵字
'''
def mode_ner_24():
    while True:
        time_epoch = int((time.time() - time_epoch_unit) / time_epoch_unit) * time_epoch_unit

        print('\033[2J\033[1;1H')

        keyword_dict = {}

        for i in range(0,289):
            tek = time_epoch - (time_epoch_unit * i)
            # print("time_epoch: %s" % datetime.fromtimestamp(tek, tz).isoformat())

            five_min_set = redis_client.zrevrange('ner_'+str(tek), 0, -1, withscores=True)

            for _w, c in five_min_set:
                w, p= re.split(",,", _w.decode("utf-8"))
                if len(w) > 1:
                    # print(_w.decode("utf-8"))
                    _c = keyword_dict.setdefault(_w.decode("utf-8"), c)
                    keyword_dict[_w.decode("utf-8")] = _c + c

        print("[24h]time_epoch: %s" % datetime.fromtimestamp(time_epoch, tz).isoformat())

        five_min_set = dict(sorted(keyword_dict.items(), key=lambda item: item[1], reverse=True))

        rank=0
        # print(five_min_set)
        for _w, c in five_min_set.items():
            # print(_w.decode("utf-8"))
            w, p= re.split(",,", _w)
            if len(w) > 1 and rank < 25:
                print("%-16s\t%-10s\t(%s)" % (w, '('+p+')', c)) # , end="\u3000"
                rank = rank + 1

        time.sleep(60)

'''
過去 一小時出現的{實體}關鍵字
'''
def mode_ner_60():
    while True:
        time_epoch = int((time.time() - time_epoch_unit) / time_epoch_unit) * time_epoch_unit

        print('\033[2J\033[1;1H')

        keyword_dict = {}

        for i in range(0,13):
            tek = time_epoch - (time_epoch_unit * i)
            # print("time_epoch: %s" % datetime.fromtimestamp(tek, tz).isoformat())

            five_min_set = redis_client.zrevrange('ner_'+str(tek), 0, -1, withscores=True)

            for _w, c in five_min_set:
                w, p= re.split(",,", _w.decode("utf-8"))
                if len(w) > 1:
                    # print(_w.decode("utf-8"))
                    _c = keyword_dict.setdefault(_w.decode("utf-8"), c)
                    keyword_dict[_w.decode("utf-8")] = _c + c

        print("[1h]time_epoch: %s" % datetime.fromtimestamp(time_epoch, tz).isoformat())

        five_min_set = dict(sorted(keyword_dict.items(), key=lambda item: item[1], reverse=True))

        rank=0
        # print(five_min_set)
        for _w, c in five_min_set.items():
            # print(_w.decode("utf-8"))
            w, p= re.split(",,", _w)
            if len(w) > 1 and rank < 25:
                print("%-16s\t%-10s\t(%s)" % (w, '('+p+')', c)) # , end="\u3000"
                rank = rank + 1

        time.sleep(60)

'''
過去五分鐘出現的{實體}關鍵字
'''
def mode_ner_5():
    while True:
        time_epoch = int((time.time() - time_epoch_unit) / time_epoch_unit) * time_epoch_unit

        print('\033[2J\033[1;1H')

        five_min_set = redis_client.zrevrange('ner_'+str(time_epoch), 0, 5, withscores=True)
        if len(five_min_set) == 0:
            time_epoch = time_epoch - time_epoch_unit
        five_min_set = redis_client.zrevrange('ner_'+str(time_epoch), 0, -1, withscores=True)

        print("[5m]time_epoch: %s" % datetime.fromtimestamp(time_epoch, tz).isoformat())

        rank=0
        for _w, c in five_min_set:
            # print(_w.decode("utf-8"))
            w, p= re.split(",,", _w.decode("utf-8"))
            if len(w) > 1 and rank < 25:
                print("%-16s\t%-10s\t(%s)" % (w, '('+p+')', c)) # , end="\u3000"
                # print("{:<10}{:<10}({:<10})".format(w, '('+p+')', c),chr(12288))
                rank = rank + 1

        time.sleep(2)
# 歐洲                       (LOC)           (6.0)
# 李妍慧                  (PERSON)        (6.0)
'''
過去五分鐘出現的關鍵字
'''
def mode_pos_5():
    while True:
        time_epoch = int((time.time() - time_epoch_unit) / time_epoch_unit) * time_epoch_unit

        print('\033[2J\033[1;1H')

        five_min_set = redis_client.zrevrange('pos_'+str(time_epoch), 0, 5, withscores=True)
        if len(five_min_set) == 0:
            time_epoch = time_epoch - time_epoch_unit
        five_min_set = redis_client.zrevrange('pos_'+str(time_epoch), 0, -1, withscores=True)

        print("[5m]time_epoch: %s" % datetime.fromtimestamp(time_epoch, tz).isoformat())

        rank=0
        for _w, c in five_min_set:
            # print(_w.decode("utf-8"))
            w, p= re.split(",,", _w.decode("utf-8"))
            if len(w) > 1 and rank < 25:
                print("%-16s\t%-10s\t(%s)" % (w, '('+p+')', c)) # , end="\u3000"
                rank = rank + 1

        time.sleep(2)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        modeArg = sys.argv[1]
        if modeArg == 'pos5':
            mode_pos_5()
        elif modeArg == 'pos60':
            pass
        elif modeArg == 'ner5':
            mode_ner_5()
        elif modeArg == 'ner60':
            mode_ner_60()
        elif modeArg == 'ner24':
            mode_ner_24()

    else:
        mode_pos_5()
    sys.exit()
