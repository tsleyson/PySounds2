import sys, os, os.path, classPySounds2

#i1 = classPySounds2.PySounds2("latin.lex", open("port.sc", "r", encoding='utf-8'))
#for word in i1.wordlist:
    #print(word)
#print()
#for category in i1.categories.keys():
    #print(category, " ", i1.categories[category])
#for rule in i1.rules:
    #print(rule)
#print()
#print(i1.getUnalteredWords())
#print(i1.applyRules())

def print_with_arrow(originalwords, newwords, outfile):
    """
    Handles output to screen and files.
    Precondition:  outfile is either a valid file path or a valid file object opened
                   in write mode; originalwords is a list of the words as they originally
                   appeared; newwords is a list of the words after undergoing change.
    Postcondition: The words will have been written to outfile like this: 'word --> new word'. 
                   If outfile already existed, its contents will have been wiped.
    """
    # The output gets all screwed up if there are blank lines in the
    # original file. Fix it.
    formattedWords = [pair[0] + ' ==> ' + pair[1] + '\n' 
        for pair in list(zip(originalwords, newwords))]
    for formattedWord in formattedWords:
        outfile.write(formattedWord)
    outfile.close()
    return formattedWords
                
def print_alone(newwords, outfile, fileonly=False):
    """
    Prints the word alone to the file.
    """
    for word in newwords:
        outfile.write(word + '\n')
    outfile.close()
    return newwords
            
def print_with_brackets(originalwords, newwords, outfile, fileonly=False):
    formattedWords = [pair[1] + ' [' + pair[0] + ']' + '\n' 
        for pair in list(zip(originalwords, newwords))]
    for formattedWord in formattedWords:
        outfile.write(formattedWord)
    outfile.close()
    return formattedWords

if __name__ == '__main__':
    changer = ''
    printmode = ''
    fonly = ''
    lexfile = ''
    scfile = ''
    if len(sys.argv) == 5:
        # We have both files, a printmode, and a file only
        lexfile = sys.argv[1]
        scfile = sys.argv[2]
        printmode = sys.argv[3]
        fonly = True if sys.argv[4] == 'True' else False
    elif len(sys.argv) == 3:
        # We have just the files; use defaults for the other two
        lexfile = sys.argv[1]
        scfile = sys.argv[2]
        changer = PySounds2(lexfile, scfile)
        printmode = '-a'
        fonly = False
    elif len(sys.argv) == 2 and sys.argv[1] == '-h':
        # We have a plea for help; print help and leave
        helpstring = ''' 
        This program is designed to take a list of words as input 
        and apply a series of changes elaborated in a separate file. It
        is based on the Sound Change Applier by Mark Rosenfelder.
        
        File names can either be given as command line arguments or 
        entered at the prompt after the program begins. Files with the
        .lex extension contain lists of words to be changed; those with 
        the .sc extension contain the rules for the changes. If the .lex 
        and .sc files aren't in the directory that you're running the 
        script from, you'll have to enter full pathnames.
        
        The changed words will be written to a .out file with the same 
        name as your .sc file. It should appear in the same directory 
        as your .sc file.
        
        For more information, see the documentation.
        '''
        print(helpstring)
    else:
        # Prompt for the files, printmode, and file only
        lexfile = input("Please enter the name of a .lex file: ")
        scfile = input("Please enter the name of a .sc file: ")
        printmode = input("Choose a printing style. Enter -a for the default. ")
        f = input("Print to screen when done? (y/n) ")
        fonly = False if f in ['y', 'Y'] else True
        
    if lexfile is not '' and scfile is not '':
        changer = classPySounds2.PySounds2(lexfile, scfile)
        
    if changer is not '':
        # Then we assume it's a properly initalized PySounds2 object and...
        cont = 'Y'
        originals = changer.getUnalteredWords()
        
        while cont in ['y', 'Y']:
            # .pso stands for 'PySounds Out' and is just mean to
            # help differentiate from the Sound Change Applier.
            out = open(os.path.splitext(scfile)[0] + '.pso', "w")
            new = changer.applyRules(scfile)
            formatted = []
            if printmode == '-a':
                formatted = print_with_arrow(originals, new, out)
            elif printmode == '-b':
                formatted = print_with_brackets(originals, new, out)
            elif printmode == '-o':
                formatted = print_alone(new, out)
            else:
                raise TypeError("Printmode not recognized.")
            if not fonly:
                for formattedWord in formatted:
                    print(formattedWord)
            cont = input("Apply the rules again? (y/n) ")
