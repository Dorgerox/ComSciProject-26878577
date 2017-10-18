import pickle
from nltk.classify import ClassifierI
from statistics import mode

# This class is used to classify a tweet using all of the classifiers
class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    # This function classifies a tweet by classifying the tweet through every classifiers and the majority
    # classification is returned
    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

# This function defines the set of features
def find_features(document):
    words = set(document)
    features = {}
    for w in wordFeatures:
        features[w] = (w in words)
    return features

# Initialise all needed classifiers and word features
wordFeatures = pickle.load(open("Classifiers/word_features.pickle", 'rb'))

NBC_classifier = pickle.load(open("Classifiers/NBC.pickle","rb"))

MNB_classifier = pickle.load(open("Classifiers/MNB.pickle","rb"))

BNB_classifier = pickle.load(open("Classifiers/BNB.pickle","rb"))

LogisticRegression_classifier = pickle.load(open("Classifiers/LR.pickle","rb"))

SGDClassifier_classifier = pickle.load(open("Classifiers/SGDC.pickle","rb"))

SVC_classifier = pickle.load(open("Classifiers/SVC.pickle","rb"))

LinearSVC_classifier = pickle.load(open("Classifiers/LSVC.pickle","rb"))

# Initialise the Voting class with all the classifiers
voted_classifier = VoteClassifier(NBC_classifier,
                                  SVC_classifier,
                                  LinearSVC_classifier,
                                  SGDClassifier_classifier,
                                  MNB_classifier,
                                  BNB_classifier,
                                  LogisticRegression_classifier)

# This function takes a tweet as input and outputs its classification
def verification(tweet):
    featuresTweet = find_features(tweet)
    return voted_classifier.classify(featuresTweet)
