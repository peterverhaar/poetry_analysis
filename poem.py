
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import os
import poetic_devices as p




file = os.path.join( 'XML' , 'DOWN_BY_THE_SALLEY_GARDENS.xml' )

ns = {'tei': 'http://www.tei-c.org/ns/1.0' }


with open( file , encoding = 'utf-8' ) as file:
    xml = file.read()



root = ET.fromstring(xml)
tei_text = root.find('tei:text/tei:body' , ns )
stanzas = tei_text.findall('tei:lg' , ns )

line_elements = []
full_text = dict()
transcriptions = dict()

if len(stanzas) > 0:
    for s in stanzas:
        lines = s.findall('tei:l' , ns )
        for l in lines:
            line_elements.append(l)
else:
    lines = tei_text.findall('tei:l' , ns )
    for l in lines:
        line_elements.append(l)


for l in line_elements:
    n_line = l.get('n')
    line_text = ''
    transcription = ''
    words = l.findall('tei:w' , ns )
    for w in words:
        line_text += w.text + ' '
        transcription += w.get('phon') + ' '
    full_text[ n_line ] = line_text.strip()
    transcriptions[ n_line ] = transcription.strip()

for t in transcriptions:
    print(transcriptions[t])
    p.alliteration( transcriptions[t] )
    rhymes = p.internal_rhyme( transcriptions[t] )

stanza = list( transcriptions.values() )
print( p.perfect_rhyme( stanza ) )
p.slant_rhyme_consonance( stanza )
print( p.slant_rhyme_assonance( stanza ) )
