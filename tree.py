import subprocess
import os
import sys
 
class tree:

	def __init__(self, id,leftChild, rightChild, sequence, consensus):
		if(leftChild == None):
			self.rightChild = None
			self.leftChild = None
			self.sequence = sequence
			self.probMatrix = generateList(sequence)
		else:
			self.rightChild = rightChild
			self.leftChild = leftChild
			self.probMatrix = generateProbMatrix(leftChild.probMatrix,rightChild.probMatrix)
			self.sequence = generateSequence(self.probMatrix)
		self.id = id
		self.upSequence = updateSequence(consensus,self.probMatrix,self.sequence)
		self.MFE = getMFEstructure(self.sequence)
		self.upMFE = getMFEstructure(self.upSequence)
		self.distance = getDistance(self.MFE,consensus)
		self.upDistance = getDistance(self.upMFE,consensus)
		self.cGContent = getCGContent(self.sequence)
		self.upCGContent = getCGContent(self.upSequence)
		self.likeliness = getMFElikeliness(self.sequence)
		self.upLikeliness = getMFElikeliness(self.upSequence)

cost = [[0.0,2.0,1.0,2.0,2.0],[2.0,0.0,2.0,1.0,2.0],[1.0,2.0,0.0,2.0,2.0],[2.0,1.0,2.0,0.0,2.0],[2.0,2.0,2.0,2.0,0.0]]
index = ['A','C','G','U','-']
validPair = [[0,3],[3,0],[1,2],[2,1],[2,3],[3,2]]

def modifyString(s,pos,newChar):
	st = list(s)
	st[pos] = newChar
	return "".join(st)

def findComplement(consensus,i):
	count = 1
	pos = i
	while(count != 0):
		pos = pos+1
		if(consensus[pos] == '('):
			count  = count + 1
		elif(consensus[pos] == ')'):
			count = count - 1
	return pos

def isValidPair(sequence,i,j):
	valid = False
	for k in range(0,len(validPair)):
		if((sequence[i] == index[validPair[k][0]]) & (sequence[j] == index[validPair[k][1]])):
			valid = True
	return valid

def getCGContent(sequence):
	count = 0.0
	for i in range(0,len(sequence)):
		if((sequence[i] == 'C') | (sequence[i] == 'G')):
			count = count+1
	return count/len(sequence)

def findBestPair(mi,mj):
	score = float("inf")
	best = 0
	for i in range(0,len(validPair)):
		b = mi[validPair[i][0]]+mj[validPair[i][1]]
		if(b < score):
			best = i
			score = b
	return best

def updateSequence(consensus,m,sequence):
	for i in range(0,len(consensus)):
		if(consensus[i] == '('):
			j = findComplement(consensus,i)
			if(isValidPair(sequence,i,j)):
				best = 0
			else:
				best = findBestPair(m[i],m[j])
				sequence = modifyString(sequence,i,index[validPair[best][0]])
				sequence = modifyString(sequence,j,index[validPair[best][1]])
	return sequence

def generateProbMatrix(left,right):
	m = []
	for i in range(0,len(left)):
		l = []
		for j in range(0,5):
			minLeft = float("inf")
			minRight = float("inf")
			for k in range(0,5):
				c = left[i][k] + cost[k][j]
				if(minLeft > c):
					minLeft = c
			for k in range(0,5):
				c = right[i][k] + cost[k][j]
				if(minRight > c):
					minRight = c
			l.append(minLeft+minRight)
		m.append(l)
	return m

def generateSequence(m):
	s = ""
	for i in range(0,len(m)):
		n = 'A'
		min = float("inf")
		for j in range(0,5):
			if(min>m[i][j]):
				n = index[j]
				min = m[i][j]
		s = s+n
	return s

def generateList(sequence):
	l = []
	for i in range(0,len(sequence)):
		b = [float('inf'),float('inf'),float('inf'),float('inf'),float('inf')]
		if(sequence[i] == 'A'):
			b[0] = 0.0
			l.append(b)
		elif(sequence[i] == 'C'):
			b[1] = 0.0
			l.append(b)
		elif(sequence[i] == 'G'):
			b[2] = 0.0
			l.append(b)
		elif(sequence[i] == 'U'):
			b[3] = 0.0
			l.append(b)
		else:
			b[4] = 0.0
			l.append(b)
	return l

def getMFEstructure(sequence):
	os.system("ECHO "+sequence+" > sequence.txt")
	structure = subprocess.check_output("RNAfold < sequence.txt", shell=True)
	structure = structure.split("\n")[1].split(" ")[0]
	return structure

def getMFElikeliness(sequence):
	os.system("ECHO "+sequence+" > sequence.txt")
	l = subprocess.check_output("RNAfold -p < sequence.txt", shell=True)
	l = float(l.split("\n")[4].split(" ")[7].split(';')[0])
	return l

def getDistance(structure,T):
	os.system("ECHO '"+T+"' > distance.txt")
	os.system("ECHO '"+structure+"' >> distance.txt")
	distance = subprocess.check_output("RNAdistance < distance.txt", shell=True)
	distance = float(distance.split(" ")[1])
	return distance