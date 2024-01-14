import csv
import datetime

from sentence_transformers import util
from torch.utils.hipify.hipify_python import bcolors
from transformers import pipeline
from fast_sentence_transformers import FastSentenceTransformer as SentenceTransformer

import backtrading

sentiment_classifier = pipeline(model="cometrain/stocks-news-t5")
sentence_transformer = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device="cpu")


def load_csv(file_path):
    with open(file_path, encoding="utf8") as csvfile:
        lines = list(csv.reader(csvfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True))
    return lines


def get_sentiment(articles):
    lines = load_csv('data/reuters_headlines.csv')

    for article in articles:
        article_list = lines[article[0]]

        x = sentiment_classifier(article_list[0])
        print(x)

        date = article_list[1].split(" ")
        if x[0]['generated_text'] == 'negative':
            print("title:", bcolors.BOLD + article_list[0], bcolors.FAIL + "negative:" + bcolors.ENDC, "\n")
            backtrading.add_date(datetime.datetime(int(date[2]), int(date[0]), int(date[1])), "NEG")
        elif x[0]['generated_text'] == 'neutral':
            print("title:", bcolors.BOLD + article_list[0], bcolors.OKBLUE + "neutral:" + bcolors.ENDC, "\n")
            backtrading.add_date(datetime.datetime(int(date[2]), int(date[0]), int(date[1])), "NEU")
        elif x[0]['generated_text'] == 'positive':
            print("title:", bcolors.BOLD + article_list[0], bcolors.OKGREEN + "positive:" + bcolors.ENDC, "\n")
            backtrading.add_date(datetime.datetime(int(date[2]), int(date[0]), int(date[1])), "POS")


def search(text, file):
    articles = []

    lines = load_csv(file)
    for row in lines:
        # if len(articles) > 1000: break
        articles.append(row[0] + ". " + row[2])

    query_emb = sentence_transformer.encode(text)
    doc_emb = sentence_transformer.encode(articles)
    scores = util.dot_score(query_emb, doc_emb)[0].tolist()
    doc_score_pairs = list(zip(list(range(0, len(articles))), scores))
    doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)

    return doc_score_pairs[:100]


def main():
    lines = load_csv('data/dataset.csv')

    articles = list
    for row in lines:
        if row[0] == ticker:
            print(row)
            articles = search(row[0] + ", " + row[1], "data/reuters_headlines.csv")
            break

    get_sentiment(articles)

    backtrading.run(ticker)


if __name__ == "__main__":
    ticker = input()
    main()
