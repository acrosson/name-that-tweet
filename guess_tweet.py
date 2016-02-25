from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn import cross_validation
from tweet_loader import TweetLoader
import numpy as np

# load tweet data from csv files
tweets = TweetLoader().load_old_tweets()
data = []
target = []

# populate target and data
for key in tweets:
    target += [key] * len(tweets[key])
    data += list(tweets[key])

# Use cross validation to split data set
X_train, X_test, y_train, y_test = cross_validation.train_test_split(data, target, test_size=0.3, random_state=0)

# Count Vectorizer
# Convert a collection of text documents to a matrix of token counts
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
X_train_counts.shape
count_vect.vocabulary_.get(u'algorithm')

# TfidfTransformer
# Transform a count matrix to a normalized tf or tf-idf representation
# Tf means term-frequency while tf-idf means term-frequency times inverse document-frequency.
# This is a common term weighting scheme in information retrieval, that has also found good use in document classification.
# The goal of using tf-idf instead of the raw frequencies of occurrence of a token in a given document
# is to scale down the impact of tokens that occur very frequently in a given corpus and that are hence
# empirically less informative than features that occur in a small fraction of the training corpus.
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)


text_clf = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                            alpha=1e-3, n_iter=5, random_state=42)),
])

# Fit training data and make prediction on test data
text_clf = text_clf.fit(X_train, y_train)
predicted = text_clf.predict(X_test)
print '################ Accuracy ################'
print np.mean(predicted == y_test)

new_prediction = text_clf.predict(["insert tweet text here"])
