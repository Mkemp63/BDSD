import json
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import requests
import os
from nltk.corpus import stopwords


def to_df(json_file_path):
    with open(json_file_path) as f:
        data = json.load(f)
    df_idf = pd.DataFrame.from_dict(data['articles'])
    return df_idf


def pre_process(text):
    # lowercase
    text = str(text).lower()

    # remove tags
    text = re.sub("</?.*?>", " <> ", text)

    # remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)

    return text


def get_stop_words(stop_file_path):
    """load stop words """

    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)


def get_column_content(column_name, df_idf):
    docs = df_idf[column_name].tolist()
    return docs


def elim_stopwords(percentage, stopwords, docs):
    cv = CountVectorizer(max_df=percentage, stop_words=stopwords)
    word_count_vector = cv.fit_transform(docs)
    return word_count_vector, cv


def compute_idf(word_count_vector):
    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    return tfidf_transformer


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    for idx, score in sorted_items:
        fname = feature_names[idx]

        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


def get_keywords(idx, tfidf_transformer, docs, cv, feature_names):
    # generate tf-idf for the given document
    tf_idf_vector = tfidf_transformer.transform(cv.transform([docs[idx]]))

    # sort the tf-idf vectors by descending order of scores
    sorted_items = sort_coo(tf_idf_vector.tocoo())

    # extract only the top n; n here is 10
    keywords = extract_topn_from_vector(feature_names, sorted_items, 5)

    return keywords


def print_results(idx, keywords, docs_title, docs_body):
    # now print the results
    print("\n=====Title=====")
    print(docs_title[idx])
    print("\n=====Body=====")
    print(docs_body[idx])
    print("\n===Keywords===")
    for k in keywords:
        print(k, keywords[k])


def main():
    # get dummy data, run once
    if not os.path.isfile('./data.json'):
        url = ('https://newsapi.org/v2/top-headlines?'
               'country=nl&'
               'apiKey=c8fbcb5d3d9c46a19f22042eb9363cc5')
        response = requests.get(url)
        print('file created')
        with open('data.json', 'w+') as outfile:
            json.dump(response.json(), outfile)

    # change json file name/path and column names
    df_idf = to_df('data.json')
    df_idf['text'] = df_idf['title'] + " " + df_idf['content']
    df_idf['text'] = df_idf['text'].apply(lambda x: pre_process(x))
    # change stopwords file name/path
    stopWords = stopwords.words('dutch')
    docs = get_column_content('text', df_idf)
    word_count_vector = elim_stopwords(85, stopWords, docs)[0]
    cv = elim_stopwords(85, stopWords, docs)[1]
    tfidf_transformer = compute_idf(word_count_vector)
    feature_names = cv.get_feature_names()
    docs_title = df_idf['title'].tolist()
    docs_body = df_idf['content'].tolist()
    i = 0
    for idx in docs:
        keywords = get_keywords(i, tfidf_transformer, docs, cv, feature_names)
        print_results(i, keywords, docs_title, docs_body)
        i += 1


if __name__ == '__main__':
    main()
