#  This script is for extracting answers from Likert-style questions exported
#  from the Coursera platform
#
#  Ryan George, December 2013
#
#  usage:
#    python likert.py <filename>
#       OR
#    ./likert.py <filename>


#!/usr/bin/env python

import string
import numpy as np
import fileinput
import sys

class Likert:

    def find_likert(self, fd):
        while True:
            line = fd.readline();
            if string.find(line, 'matrix_question') > 0:                                                                                                                    
                break
            if len(line) == 0:
                fd = []
                break
        return fd


    def par_likert(self, fd):
        #parse the likert question mess
        
        #find the start of responses
        while True:
            top_of_mq = fd.tell()
            if str.find(fd.readline(), '|') > 0: break

        #get number of questions
        nQuestions = len(string.split(fd.readline(), '|')) - 1
        fd.seek(top_of_mq)

        final_results = np.zeros((nQuestions,5))

        for line in fd:
            # go thorugh line by line and add up responses
            try:
                first_parse = string.split(line, '\t')
                nResponses = first_parse[0]
                second_parse = string.split(first_parse[1], '|')
                i = 0
                for resp in second_parse:
                    # add responses for each question

                    try:
                        #final_results[question][answer_type] should be incremented by nResponses
                        final_results[i][int(resp)-1] += int(nResponses)
                    except:
                        pass
                    i += 1
            except:
                pass

        return final_results

            
    def display_likert(self, lm):
        #given an NxM matrix from par_likert, display N questions by response
        dim = lm.shape
        q = 1
        for question in lm:
            print 'question ' + str(q) + ':'
            r = 1
            for response in question:
                print str(r) + ': ' + str(int(response))
                r += 1
            q += 1
            print '\n'


#bring up an instance of the class
L = Likert()

li = 1
#open file
fd = L.find_likert(open(sys.argv[1]))
#look through file for matrix questions, when you find one, parse and print it.
while fd != []:
    print '______Likert question #' + str(li) + ':______'
    lm = L.par_likert(fd)
    L.display_likert(lm)
    fd = L.find_likert(fd)
    li += 1
