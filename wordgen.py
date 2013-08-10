import nltk
import random as rn
from nltk.corpus import wordnet as wn
import nltk.collocations
import nltk.parse.api as prs
import math


def newword( seed, wtype = '', wierdness=(1,2)):
  posvar = list() 
  if type(wtype) == type(list()): posvar=wtype  
  #print 'making ' + str(seed) + ' type \''+str(wtype)+'\''
  if wtype == '': 
    posvar = ['n','v','a','s','r']
  elif type(wtype) == type(str()): 
    nw = list()
    for l in wtype: nw.append(l)
    posvar = nw
  if type(posvar) != type(list()): raise ValueError
#  print posvar

  worksyns = wn.synsets(seed)
#  print worksyns
  usyns=list(worksyns)
  for rec in usyns: 
    if worksyns.count(rec) > 1: worksyns.remove(rec)
    try: 
      posvar.index(str(rec.pos))
    except:
      worksyns.remove(rec)  # remove duplicates and wrong types
#  print worksyns
  synsts = list(worksyns)
#  print synsts 
  for i in range(wierdness[0]):
    for synst in synsts:
      for x in range(6):worksyns.extend(synst.hypernyms())#weight towards hypernyms
      worksyns.extend(synst.member_holonyms())
      worksyns.extend(synst.substance_holonyms())
      worksyns.extend(synst.part_holonyms())
      worksyns.extend(synst.similar_tos())
    synsts.extend(worksyns)
  usyns=list(synsts)
  for rec in usyns: 
#      print synsts.count(rec)
      if synsts.count(rec) > 1: synsts.remove(rec)
      try: 
        posvar.index(str(rec.pos))
      except:
        synsts.remove(rec)  # remove duplicates and wrong type

  #hyponyms take a long time, so reduce the number of synsets tested to 5 at most 
  if len(synsts)>5: synsts = rn.sample(synsts,5)
  for i in range(0,wierdness[1]):
    for synst in synsts:
      for x in range(6):worksyns.extend(synst.hyponyms())#weight towards hyponyms
      worksyns.extend(synst.part_meronyms())
      worksyns.extend(synst.member_meronyms())
      worksyns.extend(synst.substance_meronyms())
      worksyns.extend(synst.entailments())
    synsts.extend(worksyns)
    usyns=list(synsts)
    for rec in usyns:  
      if synsts.count(rec) > 1: synsts.remove(rec)
      try: 
        posvar.index(str(rec.pos))
      except:
        synsts.remove(rec)  # remove duplicates and wrong types
    if len(synsts)>10: synsts = rn.sample(synsts,10) #cut down to 10 before iteration
#  print 'synsts post hypo ' + str(synsts)

  #print synsts
  wordlist = list()
  for synst in synsts:
    for l in synst.lemma_names:
      wordlist.append(l)
  #print wordlist
  ulist=list(wordlist)
  for rec in ulist:  
    if wordlist.count(rec) > 1 or len(rec)>12: wordlist.remove(rec)  
  #print wordlist

  #test words for relevance, not feasible at this time

  return str(rn.sample(wordlist,1)[0])
  
def newwordlist(namelist,weirdness=(1,2)):
  rlist = list()
  for pair in namelist:
#    print pair
    rlist.append(newword(pair[0],pair[1],weirdness))
  return rlist

def syllablise(word): #breaks a word into a syllable list
  
  #split on double constonants that aren't h
  #spilt after non-doubled vowels
  #join single constonants to the syllable before
  syblist = [word[0],word[1],word[2]]
  #output list
  return syblist

def syllashuffle(word1,word2): #takes two words and shuffles the syllables
  syllist1 = syllablise(word1)
  syllist2 = syllablise(word2)
  if len(syllist1) > len(syllist2): syllist1, syllist2 = syllist2, syllist1 #syllist2 is at least as long as 1
  listlength = len(syllist2)+1  
  x=len(syllist1)
  if x > listlength/2 : x = math.floor(listlength/2)
  template = list()
  for i in range(listlength):template.append(False)
  x=int(x)
  for i in range(x):template[i]=True #make x items True
  rn.shuffle(template)
  ##Now has a shuffled true-false list and two sets of syllables. Need to map them.
  slcount1 = int(x)
  slcount2 = int(listlength-x)
  output = list()
  i = 0
  for part in template:
    sluse = syllist2
    slusec = slcount2
    if part: 
      sluse = syllist1
      slusec = slcount1
    while True:
      if len(sluse)==0: 
        break         
      prob = 1.0 / (2**(len(sluse)-slusec))
      if rn.random() < prob:
        output.append(sluse.pop())
        slusec = slusec-1
        break
      else:
        sluse.pop()
  outputstr = ''
  for s in output:
    outputstr = outputstr + str(s)
  return outputstr


#l = [('fight','nv'),('angry','a'),('man','n'),('test','')]
#a = newwordlist(l)
#print syllashuffle(a[1],a[2])
