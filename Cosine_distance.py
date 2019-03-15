import glob
import sys
import DB_Insert as dbi

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def corpify():
    corpus = []
    conn = dbi.connect_to_db()
    rows = dbi.select(conn)
    for row in rows:
        corpus.append((row[1], row[0]))
    conn.close()
    return corpus


def fit_transform_vectorizer(corpus):
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform([content for file, content in corpus])
    return tfidf_matrix


def find_similar(tfidf_matrix, index, top_n=3):
    cosine_similarities = linear_kernel(tfidf_matrix[index:index + 1], tfidf_matrix).flatten()
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
    return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]


def main():
    corpus = corpify()
    matrix = fit_transform_vectorizer(corpus)
    for index, score in find_similar(matrix, 2):
        print(score, corpus[index])


if __name__ == '__main__':
    main()
