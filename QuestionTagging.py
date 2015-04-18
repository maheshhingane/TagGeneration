#!/usr/bin/env python

from __future__ import division
import sys
import csv
import shutil

alltags=[]
queswithtag_training=[]
queswithtag_test=[]
idf_training=[]
idf_test=[]
tfidfarray=[]
tfidf_training=[]
tfidf_text=[]
test_tags=[]
temp=0
tf=0
i=0
j=0
flag=0
counter=0

#Accept command line arguments
if len(sys.argv) != 3:
    print "USAGE: python <script_name.py> <training_file> <test_file>"
    print len(sys.argv)
    sys.exit(0)
else:
    training_file = sys.argv[1]
    test_file = sys.argv[2]

#Extract unique tags from the training data
training_data = csv.reader(open(training_file,'rb'))
print "Extracting tags from training data..."
for training_row in training_data:
    counter += 1
    print "Processing row %s => question %s" %(counter,training_row[0])
    tags=training_row[3]
    test_data = csv.reader(open(test_file,'rb'))
    for tag in tags.lower().split():
        if tag not in alltags:
            alltags.append(tag)
            queswithtag_training.append([])
            queswithtag_test.append([])
            queswithtag_training[i].append(training_row[0])
            for test_row in test_data:
                if tag in test_row[1].lower() or tag in test_row[2].lower():
                    queswithtag_test[i].append(test_row[0])
            i += 1
        else:
            for j in range(len(alltags)):
                if alltags[j]==tag :
                    queswithtag_training[j].append(training_row[0])
                    for test_row in test_data:
                        if tag in test_row[1].lower() or tag in test_row[2].lower():
                            queswithtag_test[j].append(test_row[0])
print "Tags extracted successfully."


#Create the IDF array
print "Generating IDF values for training data and test data..."
for i in range(len(alltags)):
    if len(queswithtag_training[i])>0:
        idf_training.append(1/(len(queswithtag_training[i])))
    else:
        idf_training.append(0)
    if len(queswithtag_test[i])>0:
        idf_test.append(1/(len(queswithtag_test[i])))
    else:
        idf_test.append(0)
print "IDF values generated successfully."

#Create the TFIDF table
training_data = csv.reader(open(training_file,'rb'))
training_data.next()
print "Generating TFIDF values for each tag in training data..."
for row in training_data:
    for tag in row[3].lower().split():
        tf = 0
        tf += 5*(row[1].lower().count(tag))
        tf += row[2].lower().count(tag)

        for i in range(len(alltags)):
            if alltags[i]==tag:
                try:
                    temp = float(idf_training[i])
                except ValueError:
                    temp = 0
                tfidf_training.append([row[0],tag,tf*temp])
                break
print "TFIDF values generated successfully."

#Find average TFIDF value for each tag
avgtfidf_training=[]
print "Calculating average TFIDF value for each tag in training data..."
for i in range(len(alltags)):
    total = 0
    count = 0
    average = 0
    for j in range(len(tfidf_training)):
        if alltags[i]==tfidf_training[j][1]:
            total += tfidf_training[j][2]
            count += 1
    if count>0:
        average=total/count
    avgtfidf_training.append(average)
print "Average TFIDF values calculated successfully."

#Create TFIDF table for the test data
test_data = csv.reader(open(test_file,'rb'))
test_data.next()
print "Calculating TFIDF values for the test data and comparing with the average values..."
for row in test_data:
    for i in range(len(alltags)):
        tf = 0
        tf += 5*(row[1].lower().count(alltags[i]))
        tf += row[2].lower().count(alltags[i])

        try:
            temp = float(idf_test[i])
        except ValueError:
            temp = 0

        if tf*temp>0 and (tf*temp)>=avgtfidf_training[i]:
            test_tags.append([row[0],alltags[i]])
print "Tags generated for the test data successfully."

resultfile = open('result.txt','wb')
result = csv.writer(resultfile)
result.writerow(["Id","Tags"])
for i in range(len(test_tags)):
    result.writerow(test_tags[i])
#print test_tags
