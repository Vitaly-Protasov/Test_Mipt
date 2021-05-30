import re
import pandas as pd
from gensim import corpora,models,similarities
from gensim.utils import tokenize
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import pymorphy2
from tqdm import tqdm
import os
from pathlib import PurePath
from typing import List


def text_preprocess(text: str) -> List[str]:
    # lemmatize
    morph = pymorphy2.MorphAnalyzer()
    stopwords_set = set(stopwords.words('russian'))
    tokenized_text = list(tokenize(text, lowercase=True))

    cleared_text_list = []
    for word in tokenized_text:
        if word not in stopwords_set and len(word) > 1 and len(word) <= 20:
            cleared_word = re.sub(r'[^\w]', '', word).strip()
            word_lemma = morph.parse(cleared_word)[0].normal_form
            cleared_text_list.append(word_lemma)
    return cleared_text_list


def make_df_from_files(folder_names: List[str]) -> pd.DataFrame:
    df = {'file_text': [], 'file_class': []}
    for folder_name in folder_names:
        for file_name in os.listdir(folder_name):
            file_path = PurePath(folder_name, file_name)
            f = open(file_path)
            f_text = ' '.join(list(f))
            df['file_text'].append(f_text)
            df['file_class'].append(folder_name)
    return pd.DataFrame(df)


def form_corpus(df: pd.DataFrame) -> List[str]:
    corpus = []
    for i in df.file_class.unique():
        class_corpus = []
        class_corpus_lists = list(df[df.file_class == i].tokens)
        for each_text_list in class_corpus_lists:
            class_corpus += each_text_list
        corpus.append(class_corpus)
    return corpus
