from parse_data import TextParser
from utils import text_preprocess, make_df_from_files, form_corpus
from model import DummyTfIdf, get_probs_by_text
import os
import argparse
from typing import List
from pathlib import PurePath


def main(queries: str, request: str):
    query_list = queries.split('+')
    # form folders by pages of each query
    for q in query_list:
        path = PurePath(q)
        if not os.path.exists(path):
            TextParser([q])
    
    # form dataframe from files' texts
    df = make_df_from_files(query_list)
    df["tokens"] = df["file_text"].apply(text_preprocess)

    # tf-idf results
    corpus = form_corpus(df)
    classes = df.file_class.unique()
    list_dicts = DummyTfIdf(corpus, classes).compute_tfidf_dicts()

    # get probs by classes
    return get_probs_by_text(list_dicts, request)
     

if __name__ == '__main__':
    default_qus = 'Анализ почвы+Агрохимия ( удобрения, защита растений)+Плодовые растения+Овощные растения+Зерновые культуры'
    parser = argparse.ArgumentParser()
    parser.add_argument('--queries', type=str, default=default_qus)
    parser.add_argument('--request', type=str, required=True)
    args = parser.parse_args()
    probs = main(args.queries, args.request)
    for i in probs:
        print(i)
