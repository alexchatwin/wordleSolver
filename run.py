from collections import Counter
from string import ascii_uppercase
import itertools

#Load our list of 5-letter english words
with open('words.txt', 'r') as file:
    wordList = file.readlines()
    wordList = [line.rstrip().upper() for line in wordList]

#This function will perform searches for characters in words, based on a set of cases
def letterSearch(_word, _letter, _position=-1, _notPresent=False): #-1 = any position
    #case 1 return true if the letter is not present in the word
    if (_position==-1 and _notPresent==True):
        if (_word.find(_letter)==-1):
            return True
        else:
            return False
    
    #case 2 return true if the letter is present anywhere but the position specified
    if (_position>-1 and _notPresent==True):
        newWord=_word[0:_position:]+_word[_position+1::]
        print(newWord)
        if (newWord.find(_letter)>-1 and _word[_position]!=_letter):
            return True
        else:
            return False

    #case 3 return true if the letter is present in the position specified
    if(_position>-1 and _notPresent==False):
        char=_word[_position]
        if (char==_letter):
            return True
        else:
            return False

    #case 4 return true if the letter is present in any position
    if(_position==-1 and _notPresent==False):
        char=_word[_position]
        if (_word.find(_letter)>-1):
            return True
        else:
            return False

wordListLive=wordList

#1. List guesses
#Initially the Guesses list is empty, that will cause the algorithm to generate the optimal first word
#After each guess, the user needs to update the input 
Guesses=[]
Guesses.append((('A',0),('R',1),('O',1),('S',0),('E',0))) #0 is a grey cell, 1 is a yellow cell, 2 is a green cell
Guesses.append((('P',0),('O',2),('R',1),('N',0),('O',1)))
Guesses.append((('M',0),('O',2),('T',1),('O',2),('R',1)))
#Guesses.append((('A',0),('M',0),('I',2),('N',2),('E',0)))
#Guesses.append((('D',0),('J',0),('I',2),('N',2),('N',1)))
#Guesses.append((('T',1),('W',0),('I',2),('N',2),('K',0)))

#Initialise lists to store our characters which will then be used to refine the word list
known = []
present=[]
notPresent=[]

#If there are any guesses, run through the follow logic
if (len(Guesses)>0):

    for guess in Guesses:
        for i in range(len(guess)):
            letter, position = guess[i]
            if position==0:
                notPresent.append((letter, -1))
            if position==1:
                present.append((letter, i))
            if position==2:
                known.append((letter, i))
    
    #2. Strip info from guesses from wordlist

    ##Remove words with letter from not present

    for searchLetter, searchPosition in notPresent:
        result=[word for word in wordListLive if letterSearch(word, searchLetter, searchPosition, _notPresent=True)]
        wordListLive=result

    ##Remove words without wildcard letters

    for searchLetter, searchPosition in present:
        print(searchLetter)
        print(searchPosition)
        result=[word for word in wordListLive if letterSearch(word, searchLetter, searchPosition, _notPresent=True)]
        print(result)
        wordListLive=result

    ##Remove words without known position letter

    for searchLetter, searchPosition in known:
        result=[word for word in wordListLive if letterSearch(word, searchLetter, searchPosition, _notPresent=False)]
        wordListLive=result


#3. Determine 'most splitty'
#The basic concept is to check how many words contain each of the letters, 
#The 'splittiness' is defined as the fraction of the remaining word pool that words containing that letter represent
#If the splittiest letter appears in e.g. 50% of the words in the pool, guessing that letter will allow us to halve the remaining pool

def mostSplitty(_wordList):
    summary={}
    sortedSummary={}
    totalWords=len(_wordList)
    for c in ascii_uppercase:
        result=[word for word in _wordList if letterSearch(word, c, -1, _notPresent=False)]
        if result:
            summary[c]=(len(result)/totalWords)
    for w in sorted(summary, key=summary.get, reverse=True):
        sortedSummary={k: v for k, v in sorted(summary.items(), key=lambda item: item[1], reverse=True)}
    print(sortedSummary)
    return sortedSummary

#The output is a sorted list with the most splitty character at the top.
sortedSummary=list(mostSplitty(wordListLive))

#getNewWord generates all the permutations of the letters, in descending order of splittiness
#the loops will generate a candidate 'word', we then overrwrite any known characters (this could result in gibberish e.g. 'AAAAA')
#that candidate 'word' is then checked against the remaining wordlist, and the first valid word produced will be output to the user as their next guess 
def getNewWord(_sortedList, _knownLetters, _wordList):
    output=''
    for a in range(len(sortedSummary)):
        for b in range(len(sortedSummary)):
            for c in range(len(sortedSummary)):
                for d in range(len(sortedSummary)):
                    for e in range(len(sortedSummary)):
                        letters=[]
                        letters.append(sortedSummary[a])
                        letters.append(sortedSummary[b])
                        letters.append(sortedSummary[c])
                        letters.append(sortedSummary[d])
                        letters.append(sortedSummary[e])
                        for i in itertools.permutations(letters):
                            i=list(i)
                            if _knownLetters:
                                for char, p in _knownLetters:

                                    i[p]=char
                            word=''.join(i)
                            if word in _wordList:
                                output=word
                                break
                if(len(output)>0): break
            if(len(output)>0): break
        if(len(output)>0): break

    return output

print(getNewWord(sortedSummary,known, wordListLive))
