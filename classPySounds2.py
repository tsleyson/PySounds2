# PySounds2.py
# Version 2 of the PySounds class. Designed to be more modular, more complete, 
# and more flexible than both its predecessor and the original Sound Change Applier 
# from Mark Rosenfelder.

# Begun May 27 2011, almost a year after the first version was begun, several weeks 
# after the end of my last semester at Yuba College before beginning at UC Davis.

import re, _io
# _io is imported so we can test arguments to see if they're file objects.

class PySounds2:
    def __init__(self, lex, rules):
        self.processWords(lex)
        self.processRules(rules)
    # End __init__

    def processWords(self, lex):
        """
        Sets up the wordlist for the rest of the class.
        Precondition:  lex is either a valid file object, already opened in read mode, or a
                       valid file path.
        Postcondition: self.wordlist will be set to a file object, opened in read mode, that
                       ought to contain a list of words to be changed.
        Throws:        IOError for invalid file names or invalid types for lex.
        """
        if type(lex) is _io.TextIOWrapper:
            # It's an opened file object
            self.wordlist = lex
            return
        elif type(lex) is str:
            # It's a file path
            try:
                self.wordlist = open(lex, "r", encoding='UTF-8')
                return
            except IOError:
                raise IOError("From PySounds2.processWords: Invalid file path")
        else:
            raise IOError("From PySounds2.processWords: Invalid type")
    # End processWords

    def processRules(self, rules):
        """
        Sets up the rule and category members.
        Precondition:  rules is either a valid file object, already opened in read mode, or a
                       valid file path to a file with the extension '.sc'.
        Postcondition: self.categories will be have the category names defined in the file as
                       its keys, and its values will be lists of the sounds in the given category.
                       self.rules will be a list of dictionaries with the keys 'originalSound',
                       'changedSound', and 'environment', with the three parts of the rules
                       defined in the file stored as the values.
        """
        if type(rules) is str:
            # If rules is the path to the .sc file, then
            rules = open(rules, "r", encoding='utf-8')
        elif type(rules) is not _io.TextIOWrapper:
            # If it's not a string and not a file object, it's invalid and we...
            raise IOError("From PySounds2.processRules: Invalid type")

        categoryMatch = re.compile(r"""^\s*                # First match any leading whitespace
                                        ([\w\-+]{1,20}) # Allow a category name of up to twenty characters
                                        \x20?           # Allow spaces around the equals sign
                                        =               # Required
                                        \x20?
                                        (\w{1,3}        # Require one or more of up to three Unicode chars...
                                        ([\-\x20]       # ...followed by either a space or a hyphen...
                                        |               # ...or the end of the string.
                                        $))+
                                    """, re.VERBOSE)
        ruleMatch = re.compile(r"""^\s*                             # Leading whitespace
                                (\[?([\w\-+]){1,20}\]?)             # Match 1 to 20 Unicode chars, +, -, or brackets
                                \/                                  # followed by a slash (original sound)
                                ([@\w\]\[\-+]{0,20})                # Then the same again or nothing (changed sound)
                                \/
                                (!?\#?[\w\[\]\-+\(\)\']*
                                _
                                [\w\[\]\-+\(\)\']*\#?)              # Finally, match any number of Unicode chars,
                                                                    # brackets, +, -, or parentheses sandwiched
                                                                    # around an underscore (environment), with
                                                                    # optional # for initial and final position
                                                                    # and optional ! for negative rules.
                                """, re.VERBOSE)
        self.rules = []
        self.categories = {}
        for rule in rules:
            rule = rule.strip()
            if rule == '' or re.match(r"^(\s|\ufeff)*#", rule):
                continue
            elif categoryMatch.match(rule):
                # We assume we have a category definition and...
                definitionParts = rule.split('=')
                self.categories[definitionParts[0].strip()] = definitionParts[1].strip().split()
            elif ruleMatch.match(rule):
                # We probably have a rule definition, and...
                ruleParts = rule.split('/')
                self.rules.append(dict(originalSound=ruleParts[0].strip(),
                    changedSound=ruleParts[1].strip(), environment=ruleParts[2]))
            else:
                # This clause is mainly meant to bring the user's attention to lines that
                # don't contain something they need, like missing equals signs, slashes, or
                # underscores.
                raise SyntaxError("The syntax of " + rule + " is invalid.")
        rules.close()
    # End processRules

    def applyRules(self, rules=""):
        """
        Applies the rules to the words given.
        Precondition:  The self.wordlist, self.categories, and self.rules files have all been set up
                       correctly, or else the rules argument is a valid file path or opened file object
                       that can be processed by self.processRules.
        Postcondition: A list of all the words in self.wordlist with all the rules in self.rules applied
                       to them will be returned. It is the caller's responsibility to print these to the
                       screen, write them to a file, or process them further.
        """
        if rules != '':
            self.processRules(rules)
        
        expList = self.buildRules()
        originalWordlist = [word.strip() for word in self.wordlist]
        changedWordlist = []

        for word in originalWordlist:
            if word == '':
                continue
            changedWord = word
            for exp in expList:
                if len(exp) == 2:
                    changedWord = exp[0].sub(exp[1], changedWord)
                elif len(exp) == 4:
                    if exp[0].search(changedWord):
                        lastPosition = 0
                        for hit in exp[0].finditer(changedWord):
                            before = exp[2].search(hit.string[lastPosition : hit.start()])
                            if (exp[3] and not before) or (not exp[3] and before):
                                # The rule is negative and the lookbehind didn't match or it's
                                # not negative and the lookbehind matched.
                                changedWord = exp[0].sub(exp[1], changedWord, 1)
                            lastPosition = hit.end()
            changedWordlist.append(changedWord)
        self.wordlist.seek(0)
        return changedWordlist
        # End applyRules

    def buildRules(self):
        """
        Makes a list of compiled expressions.
        Precondition:  The self.categories and self.rules members have been properly intialized.
        Postcondition: A list of compiled regular expressions or tuples of the form (Boolean,
                       CompiledRegex, CompiledRegex) representing the rules will be returned.
        """
        compiledRules = []
        for rule in self.rules:
            replacedRules = self.replaceCategories(rule['originalSound'], rule['changedSound'], rule['environment'])
            compiledRules.extend(replacedRules)
        # First process the rules with self.makePattern.
        compiledRules = list(map(self.makePattern, compiledRules))

        # Next use a locally defined function (kyaah!) to compile the tuples' expressions.
        def compileTuple(patternTuple):
            """
            Compiles the strings in the return value of makePattern into regular expressions.
            Precondition:  patternTuple is either a two-tuple of the form (searchText, replacementText)
                           or a four-tuple with form (searchText, replacementText, leftContext, isNegative).
            Postcondition: A new tuple of the same form will be returned, only with the first (and third, if
                           it exists) items compiled into regular expressions.
            """
            if len(patternTuple) == 2:
                return (re.compile(patternTuple[0]), patternTuple[1])
            elif len(patternTuple) == 4:
                return (re.compile(patternTuple[0]), patternTuple[1], re.compile(patternTuple[2]), patternTuple[3])
            else:
                # Something's wrong, and we'll--
                raise TypeError("The tuple ", patternTuple, "is invalid.")
        # End compileTuple

        # Now use the locally defined function (kyaah!) with map to do the final
        # processing, and then return the list.
        compiledRules = list(map(compileTuple, compiledRules))
        return compiledRules
        # End buildRules

    def replaceCategories(self, originalSound, changedSound, environment):
        """
        Replaces categories with their component members.
        Precondition:  originalSound, environment, and changedSound must be valid expressions
                       according to PySounds syntax. In particular, all category names must be enclosed
                       in angle brackets [].
        Postcondition: If the rule implied only serial replacement of categories, a three-tuple of
                       (originalSound, changedSound, environment) is returned. If the rule needed
                       parallel replacement, a list of such tuples, one for each parallel member
                       of the category, is returned.
        """
        categoryName = re.compile(r"\[(?P<catname>.+?)\]")

        environMatches = categoryName.finditer(environment)
        for category in environMatches:
            environment = re.sub(r"(?<=\[)" + category.group('catname') + r"(?=\])",
                ''.join(self.categories[category.group('catname')]), environment)

        originalCategories = categoryName.search(originalSound)
        changedCategories = categoryName.search(changedSound)
        if originalCategories is not None and changedCategories is not None:
            envList = [environment for k in range(0, len(self.categories[originalCategories.group('catname')]))]
            originalList = [categoryName.sub(k, originalSound) for k in 
                self.categories[originalCategories.group('catname')]]
            changedList = [categoryName.sub(k, changedSound) for k in 
                self.categories[changedCategories.group('catname')]]

            # Return a list of tuples
            return list(zip(originalList, changedList, envList))
        else:
            originalMatches = categoryName.finditer(originalSound)
            for category in originalMatches:
                originalSound = re.sub(r"(?<=\[)" + category.group('catname') + r"(?=\])",
                    ''.join(self.categories[category.group('catname')]), originalSound)

            changedMatches = categoryName.finditer(changedSound)
            for category in changedMatches:
                changedSound = re.sub(r"(?<=\[)" + category.group('catname') + r"(?=\])",
                    ''.join(self.categories[category.group('catname')]), changedSound)
            # Return a list containing a single tuple.
            rtuple = originalSound, changedSound, environment
            return [rtuple]
        # End replaceCategories

    def makePattern(self, ruleTuple):
        """
        Changes PySounds metacharacters into regular expression metacharacters to make a valid
        regular expression pattern.
        Precondition:  ruleTuple is a three-tuple composed of (originalSound, changedSound, environment) like
                       what is returned from replaceCategories. This function doesn't actually use changedSound,
                       but it's easier to just pass in the return value of replaceCategories instead of making
                       a new tuple with just the original sound and environment.
        Postcondition: If the environment does not contain anything to match before the target sound, a string
                       resembling a valid regular expression pattern is returned. If the environment does contain
                       a part before the target sound, a three-tuple of (Boolean, String, String) is returned;
                       the Boolean indicates if the environment is defined negatively (True) or not (False); the
                       first string is a pattern that matches the environment before the target sound; the
                       second string is the pattern that matches the target sound and the environment after.
        """
        environment = ruleTuple[2]
        # Add a question mark to closing parentheses. This makes anything in parentheses an
        # optional group. Optional sounds don't really need to be grouped, but there's no
        # harm in it, and we save a few operations removing the parentheses. However, I
        # will change them to non-capturing parentheses to save some memory.
        environment = environment.replace('(', '(?:')
        environment = environment.replace(')', ')?')
        
        # Set isNegative to True if the environment is negative or false otherwise,
        # then get rid of the exclamation point.
        isNegative = environment[0] == '!'
        environment = environment.replace('!', '')
        
        # Replace hash marks with caret at the start or dollar sign at the end. The
        # closing parenthesis is included on the dollar sign so we don't include
        # it inside lookahead, since this won't work right if we have negative
        # lookahead.
        environment = re.sub(r"^#", "^", environment) if not isNegative else re.sub(r"^#", "(?<!^)", environment)
        environment = re.sub(r"#$", ")$", environment)

        environment = environment.split('_')
        # Now there should be two parts in the environment list: the part before the target sound
        # and the part after.
        lookaheadStart = '(?!' if isNegative else '(?='
        closingSymbol = ')' if environment[1].find('$') is -1 else ''
        if environment[0] == '' or environment[0] == '^' or environment[0] == '(?<!^)':
            return (environment[0] + ruleTuple[0] + lookaheadStart + environment[1] + closingSymbol, ruleTuple[1])
        else:
            return (ruleTuple[0] + lookaheadStart + environment[1] + closingSymbol,
                ruleTuple[1], environment[0] + '$', isNegative)
        # End makePattern

    def getUnalteredWords(self):
        """
        Returns a copy of the wordlist, unaltered.
        """
        originals = [word.strip() for word in self.wordlist]
        self.wordlist.seek(0)
        return originals
        
    def __del__(self):
        self.wordlist.close()
