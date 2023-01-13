import os
import sys
from time import sleep

import redis
import json

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
from ckiptagger import  WS, POS, NER

pos_list = ['Na', 'Nb', 'Nc', 'Ncd', 'Nd', 'Nep', 'Neqa', 'Neqb', 'Nes', 'Neu', 'Nf', 'Ng', 'Nh', 'Nv']
pos_exlist = [
    # 各式符號
    'COLONCATEGORY', 'DASHCATEGORY','DOTCATEGORY',
    'COMMACATEGORY', 'PERIODCATEGORY', 'PAUSECATEGORY',
    'ETCCATEGORY', 'EXCLAMATIONCATEGORY', 'SEMICOLONCATEGORY',
    'PARENTHESISCATEGORY', 'PAUSECATEGORY', 'QUESTIONCATEGORY',
    'SPCHANGECATEGORY', 'WHITESPACE',

    # 指代定詞
    'Nep',

    # 副詞
    'D','Da','Dfa','Dfb','Dk',

    # 介詞, 語助詞
    'P', 'T',

    # 連接詞
    'Caa', 'Cab', 'Cba', 'Cbb',

    # 語贅詞
    'DE', 'SHI', 'V_2', 'Di'
    ]


redis_client = redis.Redis('localhost', 6379, 0)

def print_word_pos_sentence(word_sentence, pos_sentence):
    assert len(word_sentence) == len(pos_sentence)
    for word, pos in zip(word_sentence, pos_sentence):
        if pos in pos_list:
            print(f"{word}({pos})", end="\u3000")
    print()

def run_process(item, ws, pos, ner):
    cache_word = []

    time_epoch = item['time_epoch']
    url = item['url']

    sentence_list = item['text']
    if item['title'] != None:
        sentence_list.append(item['title'])

    print(url)

    if len(sentence_list) == 0:
        print('='*40)
        return

    # 分詞
    word_sentence_list = ws(sentence_list)

    # 標註詞性
    pos_sentence_list = pos(word_sentence_list)

    # 標註實體
    entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

    for i, sentence in enumerate(sentence_list):

        print(f"'{sentence}'")
        print('-'*40)

        word_sentence = word_sentence_list[i]
        pos_sentence = pos_sentence_list[i]
        entity_sentence = entity_sentence_list[i]

        for word in word_sentence:
            redis_client.sadd(word, url)

        # print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i])
        assert len(word_sentence) == len(pos_sentence)
        for word, _pos in zip(word_sentence, pos_sentence):
            # if pos in pos_list and len(word) > 1 or True: # 先不做資料過濾

            if word in cache_word or _pos in pos_exlist:
                continue

            redis_client.zincrby('pos_' + str(time_epoch), 1, f"{word},,{_pos}")
            cache_word.append(word)

            print(f"{word}({_pos})", end="\u3000")

        print('\n')
        print('-'*40)

        for entity in sorted(entity_sentence):
            _, _, _ner, word = entity
            redis_client.zincrby('ner_' + str(time_epoch), 1, f"{word},,{_ner}")
            print(entity)

    print('='*40)

def main():
    # Load model without CPU
    ws = WS("./data")
    pos = POS("./data")
    ner = NER("./data")

    while True:
        _item = redis_client.rpop('ckiptagger_worker_queue')
        if _item == None:
            sleep(5)
            continue

        item = json.loads(_item)

        try:
            run_process(item, ws, pos, ner)
        except:
            print(item)
            break




def test():
    redis_client = redis.Redis('localhost', 6379, 0)

    while True:
        _item = redis_client.rpop('ckiptagger_worker_queue')
        if _item == None:
            sleep(5)
            continue
        item = json.loads(_item)
        print(item['title'])
        print(item['text'])
        print(item['tags'])
        print(item['url'])
        print('-'*40)

if __name__ == "__main__":
    main()
    sys.exit()
