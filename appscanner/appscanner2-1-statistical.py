import cPickle as pickle
from sklearn import svm, ensemble
import random
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
import numpy as np

##########
##########
    
TRAINTESTBOUNDARY = 0.75

PICKLE_NAME = 'lg-new-new-65-withnoise-statistical.p'

print 'Loading ' + PICKLE_NAME + '...'
flowlist = pickle.load(open(PICKLE_NAME, 'rb'))
print 'Done...'
print ''

print 'Flows loaded: ' + str(len(flowlist))

p = []
r = []
f = []
a = []

for i in range(50):
    ########## PREPARE STUFF
    examples = []
    trainingexamples = []
    testingexamples = []

    #classifier = svm.SVC(gamma=0.001, C=100, probability=True)
    classifier = ensemble.RandomForestClassifier()


    ########## GET FLOWS
    for package, time, flow in flowlist:
        examples.append((flow, package))
    print ''


    ########## SHUFFLE DATA to ensure classes are "evenly" distributed
    random.shuffle(examples)


    ########## TRAINING
    trainingexamples = examples[:int(TRAINTESTBOUNDARY * len(examples))]

    X_train = []
    y_train = []

    for flow, package in trainingexamples:       
        X_train.append(flow)
        y_train.append(package)

    print 'Fitting classifier...'
    classifier.fit(X_train, y_train)
    print 'Classifier fitted!'
    print ''

            
    ########## TESTING
    counter = 0
    correct = 0
        
    testingexamples = examples[int(TRAINTESTBOUNDARY * len(examples)):]

    X_test = []
    y_test = []
    y_pred = []

    for flow, package in testingexamples:   
        X_test.append(flow)
        y_test.append(package)

    #####

    y_pred = classifier.predict(X_test)

    print(precision_score(y_test, y_pred, average="macro"))
    print(recall_score(y_test, y_pred, average="macro"))
    print(f1_score(y_test, y_pred, average="macro"))
    print(accuracy_score(y_test, y_pred))
    print ''

    p.append(precision_score(y_test, y_pred, average="macro"))
    r.append(recall_score(y_test, y_pred, average="macro"))
    f.append(f1_score(y_test, y_pred, average="macro"))
    a.append(accuracy_score(y_test, y_pred))


print p
print r
print f
print a
print ''

print np.mean(p)
print np.mean(r)
print np.mean(f)
print np.mean(a)
