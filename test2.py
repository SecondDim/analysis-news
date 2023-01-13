import os
import sys
from time import sleep

import redis
import json

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
from ckiptagger import  WS, POS, NER

pos_list = ['Na', 'Nb', 'Nc', 'Ncd', 'Nd', 'Nep', 'Neqa', 'Neqb', 'Nes', 'Neu', 'Nf', 'Ng', 'Nh', 'Nv']

sentence_list = [
'原宿系誕生的日本超可愛女團「FRUITS ZIPPER」，首度訪台就空降台南跨年晚會，演出前她們緊張到不敢踏出帳 篷看現場狀況，上台前一刻看到現場數萬名觀眾整個驚嚇，在忘記手上的麥克風已經開啟的狀態下尖叫大喊，直喊「糟了！糟了！糟了」、「快哭了快哭了」，霎時間全場甚至連直播都能感受到7位女孩的緊張與驚喜。',
'「FRUITS ZIPPER」去年以一曲〈我最可愛的地方〉紅遍日本TikTok，MV瀏覽次數則突破617萬次，打入日本2022年偶像MV年度 排行榜第15名，也是唯一一組以2022年新人之姿，與各大數字女團、早安家族並駕齊驅的偶像女團，對出道僅有8個 月的她們來說，無疑是一劑超級強心針。對於這場出道後參加過觀眾最多的現場演出，每位成員都覺得有如夢境一般的不真實。',
'第一次跨年就到台南，她們抵達後馬不停蹄參加記者會與彩排，直到晚上9點才吃到真正的第一餐， 記者會上，台南市長黃偉哲不但準備水果、果乾、糕餅等各式台南美食，還精心挑選台南伴手禮包，用台南式的熱情款待遠道而來的貴客。更前往台南市美術館「南美春室The POOL」品嚐各式蛋糕與甜點，也趁機參觀美術館所展出的作品。當天演出結束後除了在後台與粉絲相見，也首次體驗台南的溫體牛肉火鍋，雖然很累但還是大喊好吃。',
'結束台南行後，「FRUITS ZIPPER」回到日本隔天馬上開始緊湊的演出行程，2月3日起則會舉辦「FRUITS ZIPPER 1st LIVE TOUR 2023 WINTER」巡迴名古屋、大阪、東京，2月12日則將挑戰能容納2000人的「LINE CUBE SHIBUYA」，而她們也希望能很快有機會來台舉辦專場演唱會，要粉絲們敬請期待。',
'日女團跨年夜萬人開唱初體驗 「上台前忘記 麥已開」心聲全都錄'
]

time_epoch = 123456

def print_word_pos_sentence(word_sentence, pos_sentence):
    assert len(word_sentence) == len(pos_sentence)
    for word, pos in zip(word_sentence, pos_sentence):
        if pos in pos_list:
            print(f"{word}({pos})", end="\u3000")
    print()

def main():
    # Load model without CPU
    ws = WS("./data")
    pos = POS("./data")
    ner = NER("./data")

    redis_client = redis.Redis('localhost', 6379, 0)

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

        # print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i])
        assert len(word_sentence) == len(pos_sentence)
        for word, pos in zip(word_sentence, pos_sentence):
            # if pos in pos_list and len(word) > 1 or True: # 先不做資料過濾
            redis_client.zincrby('pos_' + str(time_epoch), 1, word)
            print(f"{word}({pos})", end="\u3000")

        print('\n')
        print('-'*40)

        for entity in sorted(entity_sentence):
            _, _, ner, word = entity
            redis_client.zincrby('ner_' + str(time_epoch), 1, word)
            print(entity)

        print('-'*40)

    print('='*40)

if __name__ == "__main__":
    main()
    sys.exit()
