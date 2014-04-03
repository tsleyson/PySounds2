import re
from classPySounds2 import PySounds2
# mainre = re.compile(r"\w+(?=<\/b>*)");
# lb = re.compile(r"<b>$")

# match = mainre.search("My <b>cat</b>>>>>>> is furry")
# if match:
    # potentialMatch = match.group(0)
    # leftContext = lb.search(match.string[0:match.start()])
    # if leftContext:
        # print(True)
    # else:
        # print(False)

        
# This code represents the process needed to make the rule [ShortVowel]/@/!'([Consonant])([Consonant])_ happen.
# It now represents [Vowel]/@/!#_
#vm = re.compile(r"[aeiou]")
#ap = re.compile(r"\'[bcdfghjklmnpqrstvwxz]?[bcdfghjklmnpqrstvwxz]?$")
#ap = re.compile(r"\A")

def replace_with_lookbehind(word, vm, ap, isneg=False, repl=''):
    lastPos = 0
    fullWord = ""
    for match2 in vm.finditer(word):
        #print("lastPos is {0}\nmatch is {1}".format(lastPos, match2.group(0)))
        leftContext2 = ap.search(match2.string[lastPos : match2.start()])
        if (isneg and not leftContext2) or (not isneg and leftContext2) :
            # print("left context matches ", leftContext2.group(0))
            # fullWord += match2.string[lastPos : match2.end()]
            #print("String chunk is {0}".format(match2.string[lastPos : match2.end()]))
            fullWord = vm.sub(repl, match2.string, 1)
            #print(fullWord)
        # else:
            # # print("String chunk is {0}".format(match2.string[lastPos : match2.end()]))
            # # fullWord += vm.sub("@", match2.string[lastPos : match2.end()])
            # # print(fullWord)
            # #print("left context matches ", leftContext2.group(0))
            # fullWord += match2.string[lastPos : match2.end()]
        lastPos = match2.end()
    return fullWord

def take_tuple(someTuple):
    if type(someTuple) is tuple:
        return True
    return False
    
if __name__ == '__main__':
    # a = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    # print(list(map(take_tuple, a)))
    changer = PySounds2("latin.lex", "port.sc")
    wordlist = changer.applyRules()
    #print(wordlist)
    for word in wordlist:
        print(replace_with_lookbehind(word, re.compile(r"e$"), re.compile(r"[aeiou]r$")))