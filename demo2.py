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

def print_word_pos_sentence(word_sentence, pos_sentence):
    assert len(word_sentence) == len(pos_sentence)
    for word, pos in zip(word_sentence, pos_sentence):
        if pos in ['Na', 'Nb', 'Nc', 'Ncd', 'Nd', 'Nep', 'Neqa', 'Neqb', 'Nes', 'Neu', 'Nf', 'Ng', 'Nh', 'Nv']:
            print(f"{word}({pos})", end="\u3000")
    print()

def main():

    # Load model without CPU
    ws = WS("./data")
    pos = POS("./data")
    ner = NER("./data")

    while True:
        sentence = input("input:")
        sentence_list = [sentence]

        word_sentence_list = ws(sentence_list)

        pos_sentence_list = pos(word_sentence_list)
        entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

        for i, sentence in enumerate(sentence_list):
            print()
            # print(f"'{sentence}'")
            print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i])

            for entity in sorted(entity_sentence_list[i]):
                print(entity)


if __name__ == "__main__":
    main()
    sys.exit()
