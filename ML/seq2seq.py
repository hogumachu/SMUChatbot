# from tensorflow.python.keras.utils import np_utils
# from tensorflow.python.keras.layers import Dense, Activation
# import numpy as np
# from numpy import argmax
# from keras import models
# from keras import layers
# from keras import optimizers, losses, metrics
# from keras import preprocessing
# from __future__ import print_function

from keras.models import Model, load_model
from keras.layers import Input
# import numpy as np
import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
import os
import re

from konlpy.tag import Okt
from keras.models import load_model

model = load_model('ML/chatbot_model.h5')

# TAG Word
PAD = "<PADDING>"
STA = "<START>"
END = "<END>"
OOV = "<OOV>"

# Tag Index
PAD_INDEX = 0
STA_INDEX = 1
END_INDEX = 2
OOV_INDEX = 3

# Data Type
ENCODER_INPUT  = 0
DECODER_INPUT  = 1
DECODER_TARGET = 2

# MAXiMUM Sequnce
max_sequences = 30

# Embedding Vector Dimension
embedding_dim = 100

# LSTM Hidden Layer Dimension
lstm_hidden_dim = 128

# Filter
RE_FILTER = re.compile("[.,!?\"':;~()]")


words = np.load("ML/words.npy")
word_to_index = np.load("ML/word_to_index.npy", allow_pickle=True)
index_to_word = np.load("ML/index_to_word.npy", allow_pickle=True)
word_to_index = dict(enumerate(word_to_index.flatten()))[0]
index_to_word = dict(enumerate(index_to_word.flatten()))[0]
encoder_inputs = model.input[0]
encoder_outputs = model.layers[2](encoder_inputs)
encoder_outputs, state_h_enc, state_c_enc = model.layers[4](encoder_outputs)
encoder_states = [state_h_enc, state_c_enc]
encoder_model = Model(encoder_inputs, encoder_states)

decoder_inputs = model.input[1]
decoder_state_input_h = Input(shape=(lstm_hidden_dim,), name='input_3')
decoder_state_input_c = Input(shape=(lstm_hidden_dim,), name='input_4')
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_outputs = model.layers[3](decoder_inputs)
decoder_lstm = model.layers[5]
decoder_outputs, state_h_dec, state_c_dec = decoder_lstm(
    decoder_outputs, initial_state=decoder_states_inputs)
decoder_states = [state_h_dec, state_c_dec]
decoder_dense = model.layers[6]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model(
    [decoder_inputs] + decoder_states_inputs,
    [decoder_outputs] + decoder_states)


# 텍스트 생성
def generate_text(input_seq):
    # 입력을 인코더에 넣어 마지막 상태 구함
    states = encoder_model.predict(input_seq)
    # states = encoder.predict(input_seq)
    # 목표 시퀀스 초기화
    target_seq = np.zeros((1, 1))

    # 목표 시퀀스의 첫 번째에 <START> 태그 추가
    target_seq[0, 0] = STA_INDEX

    # 인덱스 초기화
    indexs = []

    # 디코더 타임 스텝 반복
    while 1:
        decoder_outputs, state_h, state_c = decoder_model.predict([target_seq] + states)

        # 결과의 원핫인코딩 형식을 인덱스로 변환
        index = np.argmax(decoder_outputs[0, 0, :])
        indexs.append(index)

        # 종료 검사
        if index == END_INDEX or len(indexs) >= max_sequences:
            break

        # 목표 시퀀스를 바로 이전의 출력으로 설정
        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = index

        # 디코더의 이전 상태를 다음 디코더 예측에 사용
        states = [state_h, state_c]

    # 인덱스를 문장으로 변환
    sentence = convert_index_to_text(indexs, index_to_word)

    return sentence

# 예측을 위한 입력 생성
def make_predict_input(sentence):
    sentences = []
    sentences.append(sentence)
    sentences = pos_tag(sentences)
    input_seq = convert_text_to_index(sentences, word_to_index, ENCODER_INPUT)

    return input_seq

def pos_tag(sentences):
    # KoNLPy 형태소분석기 설정
    tagger = Okt()

    # 문장 품사 변수 초기화
    sentences_pos = []

    # 모든 문장 반복
    for sentence in sentences:
        # 특수기호 제거
        sentence = re.sub(RE_FILTER, "", sentence)

        # 배열인 형태소분석의 출력을 띄어쓰기로 구분하여 붙임
        sentence = " ".join(tagger.morphs(sentence))
        sentences_pos.append(sentence)

    return sentences_pos

# 인덱스를 문장으로 변환
def convert_index_to_text(indexs, vocabulary):
    sentence = ''

    # 모든 문장에 대해서 반복
    for index in indexs:
        if index == END_INDEX:
            # 종료 인덱스면 중지
            break;
        if vocabulary.get(index) is not None:
            # 사전에 있는 인덱스면 해당 단어를 추가
            sentence += vocabulary[index]
        else:
            # 사전에 없는 인덱스면 OOV 단어를 추가
            sentence.extend([vocabulary[OOV_INDEX]])

        # 빈칸 추가
        sentence += ' '

    return sentence

# 문장을 인덱스로 변환
def convert_text_to_index(sentences, vocabulary, type):
    sentences_index = []

    for sentence in sentences:
        sentence_index = []

        if type == DECODER_INPUT:
            sentence_index.extend([vocabulary[STA]])

        # 문장의 단어들을 띄어쓰기로 분리
        for word in sentence.split():
            if vocabulary.get(word) is not None:
                # 사전에 있는 단어면 해당 인덱스를 추가
                sentence_index.extend([vocabulary[word]])
            else:
                # 사전에 없는 단어면 OOV 인덱스를 추가
                sentence_index.extend([vocabulary[OOV]])

        # 최대 길이 검사
        if type == DECODER_TARGET:
            # 디코더 목표일 경우 맨 뒤에 END 태그 추가
            if len(sentence_index) >= max_sequences:
                sentence_index = sentence_index[:max_sequences - 1] + [vocabulary[END]]
            else:
                sentence_index += [vocabulary[END]]
        else:
            if len(sentence_index) > max_sequences:
                sentence_index = sentence_index[:max_sequences]

        # 최대 길이에 없는 공간은 패딩 인덱스로 채움
        sentence_index += (max_sequences - len(sentence_index)) * [vocabulary[PAD]]

        # 문장의 인덱스 배열을 추가
        sentences_index.append(sentence_index)

    return np.asarray(sentences_index)