#test to read into dict
import os
import random
import wordgen

def anysimilar(list1,list2):
  flag = False
  for a in list1:
    if a in list2: flag=True
#  print str(list1)+' and '+str(list2)+' make '+str(flag)
  return flag

#open tracking file
trackerdata =list()
try:
  tracker = open('track.txt','r')
  for line in tracker:
     line=line.strip('; \n')
     trackerdata=line.split(';')
except: 
  print 'No Tracker'
  quit()
themefile = trackerdata[0]
movefile = trackerdata[1]
templatefile = trackerdata[2]
outputfilename = trackerdata[3]
numtotal = trackerdata[4]
numfinished =  trackerdata[5]
tracker.close()

#get generic theme (word,pos) pairs
genwordlist = []
try:
  genwords = open(themefile)
except: print "could not open themes file"; quit()
for line in genwords:
  line = line.strip()
  line = line.split(';')
  genwordlist.append((line[0],line[1]))

genwords.close()

movenameformats=[('as','v'),('as','n'),('v','n'),('n','v')]

#section gets weighted dictionary of possible moves
movedict = dict()

try:
  source = open(movefile)
except: print "could not open move file"; quit()

for line in source:
  sepline = line.rstrip().split(";") #split lines
  if len(sepline)<5: print "invalid input: "+str(sepline) ; quit() #5 is the minimum number of expected pieces of data per option
  linetext = line.rstrip().split(";")
  del linetext[0]
  del linetext[0]
  for i in range(int(sepline[1])): #apply weighting
    try:
      movedict[sepline[0]].append(linetext) #add to dictionary
    except KeyError:
      movedict[sepline[0]]=[linetext]
    except:
      print "error writing dictionary"
      quit()

source.close()
#print movedict

#section makes monster attribute dictionarys
for monstnum in range(int(numfinished),int(numtotal)): 

  #build moves into a monster
  #could get a template from elsewhere
  monster = dict()
  
  #pick three themes from a list
  themes = random.sample(genwordlist,3)
  #generate a tagline from the themes ' - the x y monster'
  mtagline=str()
  mname=str()
  while True:
    #print themes
    x = wordgen.newword(themes[0][0],themes[0][1])
    y = wordgen.newword(themes[1][0],themes[1][1])
    mtagline = 'the '+ (x.replace('_',' ') + ' '+ y.replace('_',' ')).title() +' Monster'
    #generate a name using words related to x and y
    #mname = wordgen.syllashuffle( wordgen.newword(x,'',(2,1)).split('_')[0] ,
    #  wordgen.newword(y,'',(2,1)).split('_')[0] )
    print mtagline
    print 'name the monster: '+ wordgen.newword(x,'',(2,1)).split('_')[0] +' '+ wordgen.newword(y,'',(2,1))
    mname = raw_input()
    mname = mname.title()
    print 'can you live with \''+mname+ ' - '+mtagline+'\'? If so, enter x'
    isit = raw_input().lower()
    if isit == 'x': break
  monster['name']= mname
  monster['tagline']= mtagline
  #random number headers
  ntem = ''
  numneeded = 10
  numsep = '  '
  for i in range(numneeded): ntem = ntem+str(random.randint(0,9))+numsep
  ntem = ntem+ str(random.randint(0,9))
  monster['nums1'] = ntem

  ntem = ''
  for i in range(numneeded): ntem = ntem+str(random.randint(0,9))+numsep
  ntem = ntem+ str(random.randint(0,9))
  monster['nums2']= ntem

##constructing the moves
  optnum = 5
  #format: action 3 is composed of an3, a13 and a23
  #  for attname in movedict.keys(): #Old way, generate optnum of each option type
  lista = ['an','a1','a2']
  for attnum in range(1,optnum+1):
    sel1 = list(random.sample(movedict[lista[1]],1)[0])
    #print movedict[lista[1]]    
    #print sel1
    sel2 = list(random.sample(movedict[lista[2]],1)[0])
    #print sel2
    #print attnum
    monster[lista[1]+str(attnum)] =  sel1[0]
    monster[lista[2]+str(attnum)] =  sel2[0]
    sel1.pop(0)
    sel2.pop(0) 
    nwords1 = list()
    nwords2 = list()
    while sel1 != list():
      word = sel1.pop(0)
      wtype = sel1.pop(0)
      nwords1.append((word,wtype))
    while sel2 != list():
      word = sel2.pop(0)
      wtype = sel2.pop(0)
      nwords2.append((word,wtype))
    allwords = list()
    allwords.extend(nwords1)
    allwords.extend(nwords2)
    allwords.extend(themes)
    allwords=list(allwords)
    startwords = list()
    endwords = list()
    random.shuffle(movenameformats)
#begin section needing user input
    while True:
      while True:
        startwords = list()
        endwords = list()
        a = [c for c in movenameformats[0][0]]
        b = [c for c in movenameformats[0][1]]
        for uword in allwords: 
          poss = [c for c in uword[1]]
          if anysimilar(a,poss): startwords.append(uword)
          if anysimilar(b,poss): endwords.append(uword)
       # print 'startwords: ' + str(startwords) + '\nendwords: '+str(endwords)
        if len(startwords)>1 and len(endwords)>1: break
        sfm=movenameformats.pop(0)
        movenameformats.append(sfm)
      #print movenameformats        
      #print 'trying again...'

      word1 = random.sample(startwords,1)[0]
      word2 = random.sample(endwords,1)[0]
      
      try:
        rnname = wordgen.newword(word1[0],movenameformats[0][0]) + ' ' + wordgen.newword(word2[0],movenameformats[0][1])
        print 'is \''+rnname +'\' a good name? type x to continue'
        isit = raw_input().lower()
        if isit=='x': print 'cool'; break
      except: 
        print 'An error occured, trying again...'
#end section needing user input
    monster['an'+str(attnum)]= rnname.replace('_',' ').title()      
    
  listb = ['rn','r1','r2']
  for attnum in range(1,optnum+1):
    sel1 = list(random.sample(movedict[listb[1]],1)[0])
    sel2 = list(random.sample(movedict[listb[2]],1)[0])
    monster[listb[1]+str(attnum)] =  sel1[0]
    monster[listb[2]+str(attnum)] =  sel2[0]
    sel1.pop(0)
    sel2.pop(0)
     
    nwords1 = list()
    nwords2 = list()
    while sel1 != list():
      word = sel1.pop(0)
      wtype = sel1.pop(0)
      nwords1.append((word,wtype))
    while sel2 != list():
      word = sel2.pop(0)
      wtype = sel2.pop(0)
      nwords2.append((word,wtype))
    allwords = list()
    allwords.extend(nwords1)
    allwords.extend(nwords2)
    allwords.extend(themes)
    startwords = list()
    endwords = list()
#begin section needing user input
    while True:
      while True:
        startwords = list()
        endwords = list()
        a = [c for c in movenameformats[0][0]]
        b = [c for c in movenameformats[0][1]]
        for uword in allwords:
          poss = [c for c in uword[1]]
          if anysimilar(a,poss): startwords.append(uword)
          if anysimilar(b,poss): endwords.append(uword)  
        if len(startwords)>1 and len(endwords)>1: break
        sfm=movenameformats.pop(0)
        movenameformats.append(sfm)
        #print movenameformats
        #print 'trying again...'
      word1 = random.sample(startwords,1)[0]
      word2 = random.sample(endwords,1)[0]
      
      try:
        rnname = wordgen.newword(word1[0],movenameformats[0][0]) + ' ' + wordgen.newword(word2[0],movenameformats[0][1])
        print 'is \''+rnname +'\' a good name? type x to continue'
        isit = raw_input().lower()
        if isit=='x': print 'okay'; break
      except: 
        print 'An error occured, trying again...'
#end section needing user input
    monster['rn'+str(attnum)]= rnname.replace('_',' ').title()
      
##--Monster Built!


#write the monster to a file
  template = open(templatefile)
  onameparts = outputfilename.split('.')
  oname = onameparts[0]+str(monstnum)
  output = open(oname+'.svg','w')
  for line in template:
    try:
      newline = line.format(monster)
      output.write(newline)
    except KeyError as e:
      print "key not found:" + str(e)
      output.write(line)
    except IOError:
      print "IO Error!"
      template.close()
      output.close()
      quit()
    except IOError:
      print "error processing:" + str(line)
      template.close()
      output.close()
      quit()
  template.close()
  output.close()
#Convert file to .pdf
  try:
    ret = os.system('inkscape \"'+oname+'.svg\" --export-area-drawing --export-text-to-path --export-dpi=300 --export-pdf=\"'+oname+'.pdf\"')
    print 'pdf made: ' + str(ret)  
  except Exception as exc:
    print str(exc)
  numfinished = str(int(numfinished)+1)
  try:
    tracker = open('track.txt','w')
    trackdata = themefile+';'+movefile+';'+templatefile+';'+outputfilename+';'+numtotal+';'+numfinished
    tracker.write(trackdata)
    tracker.close()
  except: print 'could not update tracker!'