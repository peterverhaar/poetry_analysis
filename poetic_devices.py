import re

consonants = "b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|z|D|Z|S|T|N"
vowels = "{|@|V|I|e|Q|U"
diphthongs = "aU|@U|a:|3:|i:|u:|O:|eI|aI|oI|@U|e@|I@|U@|dZ|tS"


def separatePhonemes( text ):
    phonemes = []
    text = re.sub( r'\s+' , '' , text )
    text = re.sub( r'!' , '' , text )
    text = re.sub( r'%' , '' , text )

    consonants = "bdfghjklmnprstvwzSZDT"

    regex = r'aU|@U|a:|3:|i:|u:|O:|eI|aI|oI|@U|e@|I@|U@|dZ|tS'
    regex += '|[{}]'.format(consonants)
    regex += '|[{}]'.format(vowels)

    phonemes = re.findall( regex , text )
    return phonemes


def finalPhonemeSequence( word ):
    rhyme = finalStressedSyllable( word )
    rhyme = re.sub( r'^[{}]+'.format(consonants) , '' , rhyme )
    return rhyme


def finalPhonemeSequence_line( line ):
    words = re.split( r'\s+' , line )
    last_word = words[-1]
    fps = finalPhonemeSequence(last_word)
    return fps

def finalStressedSyllable( word ):
    word = re.sub( r'\*' , '!' , word )
    parts = re.split( r'!' , word )
    rhyme = parts[-1]
    rhyme = re.sub( r'!' , '' , rhyme )
    return rhyme

def is_vowel( phoneme ):

    regex = r'{}|{}'.format( diphthongs , vowels )

    if re.search( regex , phoneme ):
        return True
    else:
        return False

def is_consonant( phoneme ):

    if re.search( r'[{}]'.format(consonants) , phoneme ):
        return True
    else:
        return False


def alliteration(tr_line):
    scheme = ''
    sounds_start = dict()
    alliterations = []


    pattern_list = []
    words = re.split( r'\s+' , tr_line )
    for w in words:
        if re.search( r'!' , w):
            syllables = re.split( '-' , w )
            for s in syllables:
                if re.search( r'^!' , s):
                    phonemes = separatePhonemes(s)
                    pattern_list.append( phonemes[0] )
                    sounds_start[ phonemes[0] ] = sounds_start.get( phonemes[0] , 0) +1
        else:
            pattern_list.append( '-' )

    for s in sounds_start:
        if sounds_start[s] > 1:
            alliterations.append(s)

    pattern = ''
    for p in pattern_list:
        if p in alliterations:
            pattern += f'{p} '
        else:
            pattern += '- '
    return pattern



## Rhyme

def perfect_rhyme( stanza ):
    # input: list of transcibed lines
    # these lines form a stanza

    # dict used to tarce repeated words
    ## repeated words are not rhymes
    word_count = dict()
    sounds_freq = dict()
    stanza_pattern = []

    for l in stanza:
        ## find last word
        words = re.split( r'\s+' , l )
        last_word = words[-1]
        fps = finalPhonemeSequence(last_word)
        ## repeated words are not rhymes
        word_count[last_word] = word_count.get( last_word , 0) + 1
        if word_count[last_word] == 1:
            sounds_freq[fps] = sounds_freq.get(fps,0)+1
            stanza_pattern.append(fps)
        else:
            stanza_pattern.append('-')


        rhyming_scheme = ''
        code = 0
        code_dict = dict()
        for line in stanza_pattern:
            if sounds_freq.get(line,0) > 1 and line not in code_dict:
                code += 1
                code_dict[line] = code

            if line in code_dict:
                rhyming_scheme += str(code_dict[line]) + ' '
            else:
                rhyming_scheme += '- '

    return rhyming_scheme



def line_ending(line):

    fps = finalPhonemeSequence_line(line)

    if re.search( r'-' , fps ):
        return 'F'
    else:
        return 'M'



def internal_rhyme( line ):
    internal_rhymes = []
    sounds_freq = dict()
    words = re.split( r'\s+' , line )

    ## deduplicate the words
    words = list( set(words) )

    for word in words:
        fps = finalPhonemeSequence(word)
        sounds_freq[fps] = sounds_freq.get(fps,0) + 1

    for s in sounds_freq:
        if sounds_freq[s] > 1:
            internal_rhymes.append(s)

    ## potential improvement: only in stressed syllables?
    return internal_rhymes

def fuzzy_matching( text ):
    ## To be completed
    a = 1

def slant_rhyme_consonance( stanza ):

    stanza_pattern = []
    sounds_freq = dict()
    words_freq = dict()
    word_pattern = dict()

    for l in stanza:
        words = re.split( r'\s+' , l )
        last_word = words[-1]

        phonemes = separatePhonemes(last_word)
        pattern = ''
        for ph in phonemes:
            if is_vowel(ph):
                pattern += '-'
            else:
                pattern += ph

        ## connect word to pattern
        word_pattern[last_word] = pattern

        sounds_freq[ pattern ] = sounds_freq.get( pattern , 0 ) + 1
        words_freq[ last_word ] = words_freq.get( last_word , 0 ) + 1
        stanza_pattern.append(last_word)

    rhyming_scheme = ''
    code = 0
    code_dict = dict()
    for line in stanza_pattern:
        pattern = word_pattern[line]

        if words_freq[line] == 1 and sounds_freq.get(pattern,0) > 1:

            if pattern not in code_dict:
                code += 1
                code_dict[pattern] = code

        if pattern in code_dict:
            rhyming_scheme += str(code_dict[pattern]) + ' '
        else:
            rhyming_scheme += '- '

    return rhyming_scheme



def slant_rhyme_assonance( stanza ):

    stanza_pattern = []
    sounds_freq = dict()
    words_freq = dict()
    fps_freq = dict()
    word_pattern = dict()

    for l in stanza:
        words = re.split( r'\s+' , l )
        last_word = words[-1]
        fps = finalPhonemeSequence(last_word)
        fps_freq[last_word] = fps_freq.get(last_word,0) +1

        phonemes = separatePhonemes(last_word)
        pattern = ''
        for ph in phonemes:
            if is_consonant(ph):
                pattern += '-'
            else:
                pattern += ph

        pattern = re.sub( r'[-]+' , '-' , pattern )

        ## connect word to pattern
        word_pattern[last_word] = pattern

        sounds_freq[ pattern ] = sounds_freq.get( pattern , 0 ) + 1
        words_freq[ last_word ] = words_freq.get( last_word , 0 ) + 1
        stanza_pattern.append(last_word)

    rhyming_scheme = ''
    code = 0
    code_dict = dict()
    for line in stanza_pattern:
        pattern = word_pattern[line]

        if words_freq[line] == 1 and sounds_freq.get(pattern,0) > 1:

            if pattern not in code_dict:
                code += 1
                code_dict[pattern] = code

        if pattern in code_dict:
            rhyming_scheme += str(code_dict[pattern]) + ' '
        else:
            rhyming_scheme += '- '

        ## remove perfect rhymes

    return rhyming_scheme
