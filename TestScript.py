import random #Get random generator
import os #operating system functions

with open("Options.txt") as f:
  lines = f.readlines() #read possible actions into list
for l in lines:
  l = l.rstrip('\n') #remove newlines

chosen = lines[random.randint(0,len(lines)-1)] #choose random option
print(chosen) #show output
newdict={'poss':chosen}
print str(newdict)
print newdict['poss']
print newdict.get('poss')

source = open("formattest.svg")
dest = open("outputtest.svg","w") #open files, w creates a new one if not found

for blah in source: #for each line
 print blah
 newblah=blah.format({'poss':'hi'}) #replace {poss} with chosen
 dest.write(newblah)

source.close()
dest.close() #close files

#The system() command takes a string, can be used to run Inkscape's command line .pdf converter.
os.system("cd ./")
quit()