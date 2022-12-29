import os
import sys

# os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Suppress as many warnings as possible
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# from tensorflow.python.util import deprecation
# deprecation._PRINT_DEPRECATION_WARNINGS = False
# import tensorflow as tf
# tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
from ckiptagger import  WS, POS, NER

def main():

    # Download data
    # data_utils.download_data_gdown("./")

    # Load model without CPU
    ws = WS("./data")
    pos = POS("./data")
    ner = NER("./data")

    # Load model with GPU
    # ws = WS("./data", disable_cuda=False)
    # pos = POS("./data", disable_cuda=False)
    # ner = NER("./data", disable_cuda=False)

    # Create custom dictionary
    # word_to_weight = {
    #     "土地公": 1,
    #     "土地婆": 1,
    #     "公有": 2,
    #     "": 1,
    #     "來亂的": "啦",
    #     "緯來體育台": 1,
    # }
    # dictionary = construct_dictionary(word_to_weight)
    # print(dictionary)

    # Run WS-POS-NER pipeline
    sentence_list = [
        "經過多年激烈戰事，複製人大戰即將結束。絶地議會派歐比王將導致戰亂的主謀者繩之以法；不料，西斯勢力已悄悄深入銀河系，勢力漸大的議長白卜庭用黑暗勢力的力量，誘惑天行者安納金轉變成黑武士達斯維達，幫助他達成心願建立銀河帝國，剷除絕地武士…【星際大戰】系列電影最後一塊拼圖，喬治盧卡斯不僅要解開黑武士的影壇跨世紀謎團，更要著手打造影史最大星際戰爭。",
    ]
    word_sentence_list = ws(sentence_list)
    # word_sentence_list = ws(sentence_list, sentence_segmentation=True)
    # word_sentence_list = ws(sentence_list, recommend_dictionary=dictionary)
    # word_sentence_list = ws(sentence_list, coerce_dictionary=dictionary)
    pos_sentence_list = pos(word_sentence_list)
    entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

    # Release model
    # del ws
    # del pos
    # del ner

    # Show results
    def print_word_pos_sentence(word_sentence, pos_sentence):
        assert len(word_sentence) == len(pos_sentence)
        for word, pos in zip(word_sentence, pos_sentence):
            print(f"{word}({pos})", end="\u3000")
        print()
        return

    for i, sentence in enumerate(sentence_list):
        print()
        print(f"'{sentence}'")
        print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i])
        for entity in sorted(entity_sentence_list[i]):
            print(entity)
    return

if __name__ == "__main__":
    main()
    sys.exit()
