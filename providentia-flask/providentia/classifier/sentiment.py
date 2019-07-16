import logging
import os
import random
import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def train_model(train_dir, app):
    logging.debug('[SENTIMENT] Training sentiment classifier')

    logging.debug('[SENTIMENT] Checking necessary NLTK resources are installed')
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')

    logging.debug('[SENTIMENT] (1/6) Loading bag of words')
    all_words, documents = load_words(train_dir)

    logging.debug('[SENTIMENT] (2/6) Obtaining frequency distribution of each adjective')
    all_words = nltk.FreqDist(all_words)
    word_features = list(all_words.keys())[:5000]

    logging.debug('[SENTIMENT] (3/6) Creating features for each review')
    feature_sets = [(find_features(rev, word_features), category) for (rev, category) in documents]

    logging.debug('[SENTIMENT] (4/6) Shuffling the documents')
    random.shuffle(feature_sets)

    logging.debug('[SENTIMENT] (5/6) Partitioning training and testing sets')
    partition_idx = int(len(feature_sets) * (4 / 5))
    training_set = feature_sets[:partition_idx]
    testing_set = feature_sets[partition_idx:]

    logging.debug('[SENTIMENT] (6/6) Preparing Naive Bayes classifier')
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    logging.debug('[SENTIMENT] Classifier accuracy percentage: ' + str(
        (nltk.classify.accuracy(classifier, testing_set)) * 100) + '%')
    # Custom method to see n most informative features as a Python list
    # pos, neg = show_most_informative_features_in_list(classifier, 100)
    with app.app_context():
        from flask import g
        if 'sentiment' not in g:
            g.sentiment = classifier


def load_words(train_dir):
    all_words = []
    documents = []
    # Load adjectives, this has shown the highest accuracy
    allowed_word_types = ["J"]

    stop_words = list(set(stopwords.words('english')))

    files_pos = os.listdir(train_dir + '/pos')
    files_pos = [open(train_dir + '/pos/' + f, 'r').read() for f in files_pos]
    files_neg = os.listdir(train_dir + '/neg')
    files_neg = [open(train_dir + '/neg/' + f, 'r').read() for f in files_neg]

    logging.debug('[SENTIMENT] Loaded training set. Tokenizing positive reviews.')

    all_pos = []
    for p in files_pos:
        # create a list of tuples where the first element of each tuple is a review
        # the second element is the label
        documents.append((p, "pos"))

        # remove punctuations
        cleaned = re.sub(r'[^(a-zA-Z)\s]', '', p)

        # tokenize
        tokenized = word_tokenize(cleaned)

        # remove stopwords
        stopped = [w for w in tokenized if w not in stop_words]

        # parts of speech tagging for each word
        pos = nltk.pos_tag(stopped)

        all_pos += pos

        # make a list of  all adjectives identified by the allowed word types list above
        for w in pos:
            if w[1][0] in allowed_word_types:
                all_words.append(w[0].lower())

    # get word cloud
    all_pos = [x[0] for x in all_pos]
    # TODO for word cloud

    logging.debug('[SENTIMENT] Tokenizing negative reviews.')

    all_neg = []
    for p in files_neg:
        # create a list of tuples where the first element of each tuple is a review
        # the second element is the label
        documents.append((p, "neg"))

        # remove punctuations
        cleaned = re.sub(r'[^(a-zA-Z)\s]', '', p)

        # tokenize
        tokenized = word_tokenize(cleaned)

        # remove stopwords
        stopped = [w for w in tokenized if w not in stop_words]

        # parts of speech tagging for each word
        neg = nltk.pos_tag(stopped)

        all_neg += neg

        # make a list of  all adjectives identified by the allowed word types list above
        for w in neg:
            if w[1][0] in allowed_word_types:
                all_words.append(w[0].lower())

    # get word cloud
    all_neg = [x[0] for x in all_neg]
    # TODO this is for word cloud

    return all_words, documents


def find_features(document, word_features):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features


def show_most_informative_features_in_list(classifier, n=10):
    """
    Return a nested list of the "most informative" features
    used by the classifier along with it's predominant labels
    """
    cpdist = classifier._feature_probdist  # probability distribution for feature values given labels
    feature_list = []
    pos_dict = {}
    neg_dict = {}
    for (fname, fval) in classifier.most_informative_features(n):
        def labelprob(l):
            return cpdist[l, fname].prob(fval)

        labels = sorted([l for l in classifier._labels if fval in cpdist[l, fname].samples()],
                        key=labelprob)
        ratio = labelprob(labels[1]) / labelprob(labels[0])
        feature_list.append([fname, labels[-1], ratio])
        if labels[-1] == "pos":
            pos_dict[fname] = ratio
        elif labels[-1] == "neg":
            neg_dict[fname] = ratio
    return pos_dict, neg_dict
