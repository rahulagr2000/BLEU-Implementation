'''
BLEU: a Method for Automatic Evaluation of Machine Translation
--------------------------------------------------------------
Implementation of BLEU: a Method for Automatic Evaluation of Machine Translation
Paper by: Kishore Papineni et. al. (IBM T. J. Watson Research Center,Yorktown Heights, NY, USA);
Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics (ACL), Philadelphia, July 2002, pp. 311-318

Date: 05/03/2016

Author: Rahul Agrawal
Dept of Computer Science, University of Southern California
Contact: rahulagr@usc.edu | Linkedin: www.linkedin.com/in/rahulagr2000
Mentor: Dr Ron Artstein, Institute of Creative Technologies, USC
Course: CS 544- Applied Natural Language Processing 
Problem Statement: http://ron.artstein.org/csci544-2016/homework-8/homework-8.html

Requirements: i. Set Gramming Size in the Code (Set to 4 by default)
	ii.  path to candidate: a single file
    iii. path to reference: a single file or a directory containing many reference files

Execution Steps: python calculatebleu.py /path/to/candidate /path/to/reference
'''

import string
import os
from glob import iglob
import sys
import math


candidate4="candidate-4/"
reference4="reference-4/"

'''
For Running on Local Machine
'''
########################
# Reading Candidate File
########################
for filepath in iglob(os.path.join(candidate4, '*.txt')): 
	with open(filepath) as f:
		data=f.read()
		canFile=data.split("\n")

##############################################
# Reading Reference File or Files in Directory
##############################################
refFile=[]
for filepath in iglob(os.path.join(reference4, '*.txt')): 
	with open(filepath) as f:
		data=f.read()
		refFile.append(data.split("\n"))

'''	
########################
# Reading Candidate File
########################
f= open(sys.argv[1],"r")
data=f.read()
canFile=data.split("\n")
print "Candidate File:", sys.argv[1]

##############################################
# Reading Reference File or Files in Directory
##############################################
refFile=[]
try:
  	f= open(sys.argv[2],"r")
	print "Reference File:",sys.argv[2]
	data=f.read()
	refFile.append(data.split("\n"))
    
except:
  	print "Reference Files:"
	for filepath in iglob(os.path.join(sys.argv[2], '*.txt')): 
		print filepath
		with open(filepath) as f:
			data=f.read()
			refFile.append(data.split("\n"))
'''

##############################################
# Function to give n grams of a input sentence
##############################################
def ngrams(input, n):
	'''
    Function to compute n gram of a input sentence
    @param: input- sentence and n- number
    @return: A dictionary of n grams and their distinct counts
    '''
	input = input.split(' ')
	if '' in input:
		input.remove('')
	output = {}
	for i in range(len(input)-n+1):
		g = ' '.join(input[i:i+n])
		output.setdefault(g, 0)
		output[g] += 1
	return output

##################################################
# Function to Compute n grams of sentence s till N
##################################################
def getNgramsTillN(s,N):
	'''
    Function to compute n gram of a input sentence
    @param: input- sentence and n- number
    @return: A dictionary of n grams and their distinct counts
    '''
	output=[]
	for i in range(1,N):
		#out = s.translate(string.maketrans("",""), string.punctuation)
		#out=out.lower()
		output.append(ngrams(s, i))
	return output

###################################################################
# SET GRAMMING SIZE HERE (Default BLEU Baseline is 4 grams, max 10)
N= 4
###################################################################

precision=[[],[],[],[],[],[],[],[],[],[]] 
numerator,denominator=[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]
r,c=0,0
canLengthList,refLengthList=[],[]

#For each sentence in the candidate file, do the following	
for sentenceNo in range(len(canFile)):
	candidate= canFile[sentenceNo]
	reference=[]
	for i in refFile:
		reference.append(i[sentenceNo])
	
    # Get the gramming of candidate sentence till N
	listGrams=getNgramsTillN(candidate,N+1) 
	
    # For all grams till N, repeat
	for j in range(N):
		can1= listGrams[j]
		if (j==0):
			canLength= sum(can1.values())
			canLengthList.append(canLength)

		ref1=[]
		for i in reference:
			ref1.append(getNgramsTillN(i,N+1)[j])
		ref=ref1[0]
		if j==0:
			refLength=sum(ref.values())
			temp=refLength

		for i in ref1[1:]:
			if j==0:
				refLength=sum(i.values())
				if abs(canLength-refLength)<abs(canLength-temp):
					temp=refLength
			for k,v in i.items():
				if k in ref:
					ref[k]=max(v,ref[k])
				else:
					ref[k]=v
		if j==0:
			refLengthList.append(temp)
		
		d = {x:min(can1[x],ref[x]) for x in can1 if x in ref}
		
		numerator[j]=numerator[j]+sum(d.values())
		denominator[j]=denominator[j]+sum(can1.values())    
            

print "Clipped CR Counts:",numerator,"\nCandidate Counts: ",denominator

# Calculating BLEU Scores: See paper for formula
bleu=0.0
for i in range(len(numerator)):
	if numerator[i]!=0 and denominator[i]!=0:
		bleu=bleu+float(math.log((float(numerator[i])/float(denominator[i]))))
        
# Refer to the paper for meaning of c and r
c= sum(canLengthList)
r= sum(refLengthList)
print "c=",c,"   r=",r

# Calculating Brevity Penalty
BP=min(1-(float(r)/c),0)
print"Brevity Penalty= ",BP 

bleu= math.exp(float(bleu/N) + BP)
print "Bleu Score=", bleu,"\n"

# Writing values in file
f= open("bleu_out.txt","w")
f.write(str(bleu))
f.close()
