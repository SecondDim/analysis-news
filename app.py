import os
import sys
from time import sleep

import redis
import json

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
from ckiptagger import  WS, POS, NER

def print_word_pos_sentence(word_sentence, pos_sentence):
    assert len(word_sentence) == len(pos_sentence)
    for word, pos in zip(word_sentence, pos_sentence):
        if pos in ['Na', 'Nb', 'Nc', 'Ncd', 'Nd', 'Nep', 'Neqa', 'Neqb', 'Nes', 'Neu', 'Nf', 'Ng', 'Nh', 'Nv']:
            print(f"{word}({pos})", end="\u3000")
    print()

def main():
    redis_client = redis.Redis('localhost', 6379, 0)

    # Load model without CPU
    ws = WS("./data")
    pos = POS("./data")
    ner = NER("./data")

    while True:

        _item = redis_client.rpop('ckiptagger_worker_queue')
        if _item == None:
            sleep(60)
            continue

        item = json.loads(_item)
        sentence_list = item['text']

        word_sentence_list = ws(sentence_list)

        pos_sentence_list = pos(word_sentence_list)
        entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

        for i, sentence in enumerate(sentence_list):
            print()
            # print(f"'{sentence}'")
            print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i])

            for entity in sorted(entity_sentence_list[i]):
                print(entity)

def test():
    redis_client = redis.Redis('localhost', 6379, 0)

    while True:
        _item = redis_client.rpop('ckiptagger_worker_queue')
        if _item == None:
            sleep(5)
            continue
        item = json.loads(_item)
        print(item['title'])
        print(item['tags'])
        print(item['url'])
        print('-'*40)

if __name__ == "__main__":
    test()
    sys.exit()
