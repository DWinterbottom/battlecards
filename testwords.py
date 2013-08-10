import nltk
from nltk.corpus import wordnet as w

try:
  genwords = open("themes.txt")
except: print "could not open themes file"; quit()
for line in genwords:
  line = line.strip()
  line = line.split(';')
  apos = [c for c in line[1]]
  synlist = w.synsets(line[0])
  flag = True
  for c in apos  :
    for synst in synlist:
      if synst.pos == c: flag = False
    if flag: print 'no '+c+' found for '+line[0]+'\n'+str(synlist)+'\n'
genwords.close()

try:
  moves = open("movelist.txt")
except: print "could not open move file"; quit()
for line in moves:
  line = line.strip()
  line = line.split(';')
  line.pop(0)
  line.pop(0)
  line.pop(0)
  apos = [c for c in line[1]]
  synlist = w.synsets(line[0])
  flag = True
  for c in apos:  
    for synst in synlist:
      if synst.pos == c: flag = False
    if flag: print 'no '+c+' found for '+line[0]+'\n'+str(synlist)+'\n'
moves.close()