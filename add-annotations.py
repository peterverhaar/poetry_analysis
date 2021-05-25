
import re
import os
from nltk import word_tokenize
import nltk
from nltk.stem import WordNetLemmatizer
import re


def ptb_to_wordnet(PTT):

    if PTT.startswith('J'):
        ## Adjective
        return 'a'
    elif PTT.startswith('V'):
        ## Verb
        return 'v'
    elif PTT.startswith('N'):
        ## Noune
        return 'n'
    elif PTT.startswith('R'):
        ## Adverb
        return 'r'
    else:
        return ''


lemmatiser = WordNetLemmatizer()

tei_start = '''<?xml version="1.0" encoding="UTF-8"?>
		<TEI xsi:schemaLocation="http://www.tei-c.org/ns/1.0 http://www.let.leidenuniv.nl/wgbw/DMT/tei_BTCP.xsd" xmlns="http://www.tei-c.org/ns/1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
		<teiHeader>
		<fileDesc>
		<titleStmt>
		<title>$title</title>
		<title type="gmd">[electronic resource]</title>
		<author>Louis MacNeice</author>
		<principal>Peter Verhaar</principal>
		<respStmt>
		<resp>Creation of machine-readable version: </resp>
		<name>Peter Verhaar</name></respStmt>
		<respStmt>
		<resp>Conversion to TEI.2-conformant markup: </resp>
		<name>Peter Verhaar</name></respStmt>
		</titleStmt>
		<publicationStmt>
		<publisher>Leiden University</publisher>
		<pubPlace>Leiden, Netherlands</pubPlace>
		<address>
		<addrLine>P.O. Box 9515</addrLine>
		<addrLine>2300 RA Leiden</addrLine>  </address>
		<date>2021</date> </publicationStmt>
		<sourceDesc>
		<biblFull>
		<titleStmt>
		<title>$title</title></titleStmt>
		 <publicationStmt>
		  <publisher>Faber and Faber</publisher>
		 </publicationStmt>
		</biblFull> </sourceDesc>  </fileDesc>
		 </teiHeader>
		<text>

		<body>'''

tei_end =	'''</body>
		   </text>
		</TEI>
		'''


## Read pronunication dictionary
pronunciation_dict = dict()
file = open('pronunciationDictionary.txt' , encoding = 'utf-8')
for line in file:
	parts = re.split( r'\t' , line )
	pronunciation_dict[ parts[0] ] = parts[1]

dir = 'Yeats'

if not os.path.isdir('XML'):
	os.mkdir('XML')


texts = []

for root, dirs, files in os.walk(dir):
	for file in files:
		if re.search( r'\.txt$' , file ):
			texts.append( os.path.join(root, file) )

def encodeFileName(text):
	text = re.sub( r'[\'`]' , '&#x27;' , text)
	text = re.sub( r'\s+' , '_' , text)
	return text



def encode_line(line):
	encoded_line = ''
	words = word_tokenize(line)
	pos = nltk.pos_tag(words)

	for i in range( 0 , len(words) ):
		encoded_line += '\n<w '
		word = words[i]
		encoded_line += f'pos="{pos[i][1]}" '

		lemma = ''
		posTag = ptb_to_wordnet( pos[i][1] )
		if re.search( r'\w+' , posTag , re.IGNORECASE ):
			lemma = lemmatiser.lemmatize( words[i] , posTag )
		else:
			lemma = lemmatiser.lemmatize( words[i] )
		encoded_line += f'lemma="{lemma}" '
		transcr = pronunciation_dict.get( word.lower() , "" )
		transcr = re.sub( r'["]' , '!' , transcr )
		encoded_line += f'phon="{ transcr  }" '

		encoded_line += '>'
		encoded_line += f'{ word }</w> '
	return encoded_line



for text in texts:
	print(text)
	out_file = os.path.basename(text)
	out_file = re.sub( 'txt$' , 'xml' , out_file )
	out_file = encodeFileName(out_file)
	out = open( os.path.join( 'XML' , out_file ) , 'w' , encoding='utf-8' )

	with open( text , encoding  = 'utf-8') as fh:
		full_text = fh.read()
		full_text = full_text.strip()

	segments = re.split( r'\n' , full_text )
	title = segments[0]
	del segments[0]

	lines = dict()
	n_line = 0
	n_stanza = 0
	open_stanza = False

	body = ''

	for index in range( 0 , len(segments) ):
		line = segments[index]
		if re.search( r'.' , line):
			n_line += 1
			body += f'\n<l n="{n_line}">{ encode_line(line) }</l>'
		else:
			if n_line > 0:
				body += '</lg>'

			n_stanza += 1
			body += f'\n<lg n="s{n_stanza}">'

	body += '\n</lg>'

	out.write( tei_start )
	out.write( f'<head><title>{title}</title></head>')
	out.write(body)
	out.write( tei_end )
