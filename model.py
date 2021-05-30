from collections import Counter
import numpy as np
from tqdm import tqdm
from typing import List, Dict


class DummyTfIdf:
    def __init__(self, corpus: List[List[str]]):
        self.corpus = corpus
        self.len_corpus = len(corpus)

    def __compute_tf(self, text: List[str]) -> None:
        tf_text = Counter(text)
        for i in tf_text:
            tf_text[i] = tf_text[i]/float(len(text))
        return tf_text

    def __compute_idf(self, word: str) -> float:
        return np.log10(self.len_corpus/sum([1.0 for i in self.corpus if word in i])) + 1
    
    def compute_tfidf(self) -> List[Dict[str, float]]:
        documents_list = []
        for text in tqdm(self.corpus):
            tf_idf_dictionary = {}
            computed_tf = self.__compute_tf(text)
            for word in computed_tf:
                tf_idf_dictionary[word] = computed_tf[word] * self.__compute_idf(word)
            documents_list.append(tf_idf_dictionary)
        return documents_list
