from collections import Counter
from msilib import knownbits
from string import ascii_uppercase
import itertools
from xml.etree.ElementPath import prepare_descendant


wordListUpper=[]

with open('words.txt', 'r') as file:
    wordList = file.readlines()
    wordList = [line.rstrip().upper() for line in wordList]

#wordList=['HELLO', 'AMBER', 'EMBER']

def letterSearch(_word, _letter, _position=-1): #-1 = any position
    if _position==-1:
        pos=_word.find(_letter)
    else:
        pos=_word.find(_letter, _position)

    if (pos==-1):
        return False
    if (pos==_position or _position==-1):
        return True
    else:
        return False

def letterCount(_word):
    return Counter([char for char in _word])        

wordListLive=wordList
searchLetterList=[('E',3), ('A', -1)]
for searchLetter, searchPositon in searchLetterList:
    result=[word for word in wordListLive if letterSearch(word, searchLetter, searchPositon)]
    wordListLive=result
print(len(wordList))
print(len(wordListLive))


#wordList=['HELLO', 'AMBER', 'EMBER']
wordListLive=wordList
#1. List guesses
#(('R',1),('U',0),('I',0),('N',0),('S',0))
Guesses=[]
Guesses.append((('A',0),('R',1),('O',1),('S',0),('E',0)))
Guesses.append((('N',0),('I',0),('T',1),('R',1),('O',1)))
Guesses.append((('T',1),('H',0),('R',1),('O',2),('B',1)))
#Guesses.append((('A',0),('M',0),('I',2),('N',2),('E',0)))
#Guesses.append((('D',0),('J',0),('I',2),('N',2),('N',1)))
#Guesses.append((('T',1),('W',0),('I',2),('N',2),('K',0)))
known = []
present=[]
notPresent=[]
if (len(Guesses)>0):




    for guess in Guesses:
        for i in range(len(guess)):
            letter, position = guess[i]
            if position==0:
                notPresent.append((letter, -1))
            if position==1:
                present.append((letter, -1))
            if position==2:
                known.append((letter, i))
    
    #2. Strip info from guesses from wordlist

    

    ##Remove words with letter from not present

    for searchLetter, searchPosition in notPresent:
        result=[word for word in wordListLive if letterSearch(word, searchLetter, searchPosition)==False]
        wordListLive=result

    ##Remove words without wildcard letters

    for searchLetter, searchPosition in present:
        result=[word for word in wordListLive if letterSearch(word, searchLetter, searchPosition)]
        wordListLive=result

    #Remove words without known position letter

    for searchLetter, searchPosition in known:
        result=[word for word in wordListLive if letterSearch(word, searchLetter, searchPosition)]
        wordListLive=result

    #print(wordListLive)

#3. Determine most splitty 

def mostSplitty(_wordList):
    summary={}
    sortedSummary={}
    totalWords=len(_wordList)
    for c in ascii_uppercase:
        result=[word for word in _wordList if letterSearch(word, c)]
        if result:
            summary[c]=(len(result)/totalWords)
    for w in sorted(summary, key=summary.get, reverse=True):
        sortedSummary={k: v for k, v in sorted(summary.items(), key=lambda item: item[1], reverse=True)}
    print(sortedSummary)
    return sortedSummary


sortedSummary=list(mostSplitty(wordListLive))

knownLetters=["","","","",""]
print(sortedSummary)




def getNewWord(_sortedList, _knownLetters):
    for a in range(len(sortedSummary)):
        for b in range(len(sortedSummary)-1):
            for c in range(len(sortedSummary)-2):
                for d in range(len(sortedSummary)-3):
                    for e in range(len(sortedSummary)-4):
                        letters=[]
                        letters.append(sortedSummary[a])
                        letters.append(sortedSummary[b+1])
                        letters.append(sortedSummary[c+2])
                        letters.append(sortedSummary[d+3])
                        letters.append(sortedSummary[e+4])
                        print(letters)
                        for i in itertools.permutations(letters):
                            i=list(i)
                            if _knownLetters:
                                for char, p in _knownLetters:

                                    i[p]=char
                            word=''.join(i)
                            if word in wordList:
                                return word
    else:
        return 'NULL'

print(getNewWord(sortedSummary,known))
