import tree

def parser(filename):
	stock = filename
	f = open(stock,'r')
	sequences = {}
	consensus = ""
	for line in f:
		if((line[0] != '#') & (line[0] != '/')):
			sequences[line.split(' ')[0].split('\n')[0]] = line.split(' ')[1].split('\n')[0]
	f.seek(0)
	for line in f:
		a = line.split(' ')
		if(len(a)>1):
			if(a[1] == "SS_cons"):
				consensus = a[2]
	return [sequences,consensus]

def modifyConsensus(consensus):
	new = ""
	for i in range(0,len(consensus)):
		if(consensus[i] == '<'):
			new = new + '('
		elif(consensus[i] == '>'):
			new  = new + ')'
		else:
			new  = new + '.'
	return new
a = parser("RprA.txt")
consensus = modifyConsensus(a[1])
sequences = a[0]
leaves = ['BX950851.1/2106268-2106157','AP008232.1/2390532-2390429','AALD02000007.1/58628-58520','020AALF00003.1/16089-16192','AALD02000007.1/58628-58520','AALC02000001.1/49739-49635','AAYT01000004.1/252910-253019','BX571867.1/288515-288628']
internal = [[0,1],[3,4],[5,9],[2,10],[6,11],[7,12],[8,13]]
nodes = []
for i in range(0,len(leaves)):
	nodes.append(tree.tree(i,None,None,sequences[leaves[i]],consensus))
for i in range(0,len(internal)):
	nodes.append(tree.tree(i+len(leaves),nodes[internal[i][0]],nodes[internal[i][1]],None,consensus))

g = open("RprAR.csv",'w')
g.write("length of sequences, number of sequences,consensus\n")
g.write(""+str(len(nodes[0].sequence))+','+str(len(leaves))+','+str(consensus)+"\n")
g.write("id,MFE structure,MFE structure new,distance,distance new,CG content,CG content new,probability of MFE structure,probability of MFE structure new\n")
for i in range(0,len(nodes)):
	n = nodes[i]
	g.write(""+str(n.id)+','+str(n.MFE)+','+str(n.upMFE)+','+str(n.distance)+','+str(n.upDistance)+','+str(n.cGContent)+','+str(n.upCGContent)+','+str(n.likeliness)+','+str(n.upLikeliness)+"\n")

