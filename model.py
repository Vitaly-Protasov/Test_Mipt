from collections import Counter
import numpy as np
from tqdm import tqdm
from typing import List, Dict, Tuple


class DummyTfIdf:
    def __init__(self, corpus: List[List[str]], class_names: List[str]):
        self.corpus = corpus
        self.len_corpus = len(corpus)
        self.class_names = class_names

    def __compute_tf(self, text: List[str]) -> None:
        tf_text = Counter(text)
        for i in tf_text:
            tf_text[i] = tf_text[i]/float(len(text))
        return tf_text

    def __compute_idf(self, word: str) -> float:
        return np.log10(self.len_corpus/sum([1.0 for i in self.corpus if word in i])) + 1
    
    def compute_tfidf_dicts(self) -> List[Dict[str, Dict[str, float]]]:
        documents_list = []
        for text, class_name in tqdm(zip(self.corpus, self.class_names)):
            tf_idf_dictionary = {}
            computed_tf = self.__compute_tf(text)
            for word in computed_tf:
                tf_idf_dictionary[word] = computed_tf[word] * self.__compute_idf(word)
            documents_list.append({class_name: tf_idf_dictionary})
        return documents_list


def get_probs_by_text(
    list_dicts_after_tfidf: List[Dict[str, Dict[str, float]]],
    new_text: str
) -> List[Tuple[str, float]]:
    scores = {}
    for term_dict in list_dicts_after_tfidf:
        name_class = next(iter(term_dict))
        class_tfidf_dict = term_dict[name_class]
        if name_class not in scores:
            scores[name_class] = 0

        for w in text_preprocess(new_text):
            if w in class_tfidf_dict:
                scores[name_class] += class_tfidf_dict[w]

    sorted_scores = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    return sorted_scores
