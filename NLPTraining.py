import nltk
import random
import pickle
from nltk.corpus import stopwords
"""
This module was based off a tutorial that can be found at this link:
https://pythonprogramming.net/combine-classifier-algorithms-nltk-tutorial/
This tutorial describes how to create a sentiment analysis system using Twitter data.
This incorporates creating, training and loading classifiers to be used.
"""

# Initialises all need variables
f = open("trainingdata.txt", 'r')
t = open("posorneg.text", 'r')
counter = 0
documents = []
posornegArray = t.readlines()
trainingArray = f.readlines()

# Creating a document where the tweet is next to its classification
for tweet in trainingArray:
    documents.append((tweet.split(), posornegArray[counter].rstrip()))
    counter += 1

# This code is used when there is new training data
# all_words = []
#
# for w in trainingArray:
#     for j in w.split():
#         if j not in stopwords.words('english'):
#             all_words.append(j)
#
# all_words = nltk.FreqDist(all_words)
#
# wordFeatures = list(all_words.keys())
#
# save_word_features = open("Classifiers/word_features.pickle", "wb")
# pickle.dump(wordFeatures, save_word_features)
# save_word_features.close()


wordFeatures = pickle.load(open("Classifiers/word_features.pickle", "rb"))

# This function defines the set of features
def find_features(document):
    words = set(document)
    features = {}
    for w in wordFeatures:
        features[w] = (w in words)
    return features


# Create a feature set from each tweet in the document
featuresets = [(find_features(rev), category) for (rev, category) in documents]

# Load all all of the classifiers from the saved pickle files
NBC_classifier = pickle.load(open("Classifiers/NBC.pickle", "rb"))

MNB_classifier = pickle.load(open("Classifiers/MNB.pickle", "rb"))

BNB_classifier = pickle.load(open("Classifiers/BNB.pickle", "rb"))

LogisticRegression_classifier = pickle.load(open("Classifiers/LR.pickle", "rb"))

SGDClassifier_classifier = pickle.load(open("Classifiers/SGDC.pickle", "rb"))

SVC_classifier = pickle.load(open("Classifiers/SVC.pickle", 'rb'))

LinearSVC_classifier = pickle.load(open("Classifiers/LSVC.pickle", "rb"))

# Main testing section. Train on the training set and then test the classifiers on the testing set
for i in range(1):
    random.shuffle(featuresets)
    # Set that we'll train our classifier with
    trainingSet = featuresets[:round(len(documents) * 0.5)]

    # Set that we'll test against.
    testingSet = featuresets[round(len(documents) * 0.5):]

    # Here are the all the classifiers I will use
    NBC_classifier.train(trainingSet)
    print("Classifier accuracy percent:", (nltk.classify.accuracy(NBC_classifier, testingSet)) * 100)

    MNB_classifier.train(trainingSet)
    print("MultinomialNB accuracy percent:", nltk.classify.accuracy(MNB_classifier, testingSet) * 100)

    BNB_classifier.train(trainingSet)
    print("BernoulliNB accuracy percent:", nltk.classify.accuracy(BNB_classifier, testingSet) * 100)

    LogisticRegression_classifier.train(trainingSet)
    print("LogisticRegression_classifier accuracy percent:",
          (nltk.classify.accuracy(LogisticRegression_classifier, testingSet)) * 100)

    SGDClassifier_classifier.train(trainingSet)
    print("SGDClassifier_classifier accuracy percent:",
          (nltk.classify.accuracy(SGDClassifier_classifier, testingSet)) * 100)

    SVC_classifier.train(trainingSet)
    print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testingSet)) * 100)

    LinearSVC_classifier.train(trainingSet)
    print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testingSet)) * 100)

# After they have been all trained, save them back in the pickle files
save_classifier = open("Classifiers/NBC.pickle", "wb")
pickle.dump(NBC_classifier, save_classifier)
save_classifier.close()

save_classifier = open("Classifiers/MNB.pickle", "wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

save_classifier = open("Classifiers/BNB.pickle", "wb")
pickle.dump(BNB_classifier, save_classifier)
save_classifier.close()

save_classifier = open("Classifiers/LR.pickle", "wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()

save_classifier = open("Classifiers/SGDC.pickle", "wb")
pickle.dump(SGDClassifier_classifier, save_classifier)
save_classifier.close()

save_classifier = open("Classifiers/SVC.pickle", "wb")
pickle.dump(SVC_classifier, save_classifier)
save_classifier.close()

save_classifier = open("Classifiers/LSVC.pickle", "wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()

