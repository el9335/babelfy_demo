import os
import babelDisamb

global dictoccupation, listoccupation, dicttask, listtask

def makeFilePaths():
	
	#build path to O*NET
	x = os.getcwd()
	y = '/onet_db_19_0'
	z = x + y

	if os.path.exists(z):
		print("O*NET directory " + z + " found.")
	else:
		print("Error: O*NET directory " + z + " not found.")


	f1 = z + '/Occupation Data.txt'
	f2 = z + '/Task Statements.txt'

	if os.path.isfile(f1):
    		print("O*NET file /one_db_19_0/Occuption Data.txt exists.")
	else:
    		print("Error: O*NET file /one_db_19_0/Occuption Data.txt not found.")
	if os.path.isfile(f2):
    		print("O*NET file /one_db_19_0/Task Statements.txt exists")
	else:
    		print("Error: O*NET file /one_db_19_0/Task Statements.txt not found.")

    	return z

def buildOccupationDict(p):
	
	print "\nBuilding occupation dictionary..."

	dictoccupation = {}
	listoccupation = []

	f1 = p + '/Occupation Data.txt'

	ff1 = open(f1, mode = 'r')
	
	x = ff1.readline() # skip header line
	y = 0
	c1 = "\t"
	occupation_code = 0
	occupation_description = ""

	try:
		while True:
			x = ff1.readline()
			y = y + 1

			if x != "":
				i1 = x.find(c1)
				occupation_code = x[0:i1]
				
				x = x[i1+1:]
				i1 = x.find(c1)
				occupation_title = x[0:i1]

				x = x[i1+1:]
                		i1 = x.find(c1)
                		occupation_description = x[0:i1]
	
				if occupation_code in dictoccupation:
					z = dictoccupation[occupation_code]
					z[0] = z[0] + 1	
				else:
					dictoccupation[occupation_code] = [1, occupation_title, occupation_description]

			else: 
				break
	except UnicodeDecodeError:
		print("UnicodeDecodeError:", y)
	ff1.close()

	print("Occupation dictionary built.")

	for i in dictoccupation:
		listoccupation.append([i,dictoccupation[i][0]])

	listoccupation.sort(key=lambda n: n[1], reverse=True)

	print("Occupation list sorted.")

	return listoccupation

def buildTaskDict(p):
	print ("\nBuilding Task Dictionary...")

	f2 = p + '/Task Statements.txt'

	dicttask = {}
	listtask = []

	ff2 = open(f2, mode = 'r')
	x = ff2.readline()
	y = 0

	c1 = "\t"
	occupation_code = 0
	task_code = 0
	task_description = ""

	try:
		while True:
			x = ff2.readline()	
			y = y + 1

			if x != "":
				i1 = x.find(c1)
				occupation_code = x[0:i1]
				
				x = x[i1+1:]
				i1 = x.find(c1)
				task_code = x[0:i1]
				x = x[i1+1:]
		                i1 = x.find(c1)
                		task_description = x[0:i1]
                            
                		if task_code in dicttask:
                    			z = dicttask[task_code]
	                                z[0] = z[0] + 1
                    			z[1] = z[1] + [occupation_code]
                		else:
					#dicttask[task_code] = [1, [occupation_code], task_description]
                    			dicttask[task_code] = task_description

            		else:
                		break
    	except UnicodeDecodeError:
        	print("UnicodeDecodeError:", y)
    	
    	ff2.close()


	print ("Task Dictionary built.")
	for i in dicttask:
		listtask.append([i,dicttask[i][0]])

	listtask.sort(key=lambda n: n[1], reverse=True)
	
	print ("Task list sorted.")				

	#run first three tasks through babelfy
	for key in sorted(dicttask)[:3]:
		run = 'python babelDisamb.py -a -all "' + str(dicttask[key]) + '"' 		
		#print str(dicttask[key])
	        #print run
		os.system(run)
	
	return listtask

if __name__ == '__main__':


	path = makeFilePaths()

	buildOccupationDict(path)
	buildTaskDict(path)
