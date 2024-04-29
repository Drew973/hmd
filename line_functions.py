# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 08:40:36 2024

@author: Drew.Bennett
"""


'''
    read HMSTART line.
    str -> dict
'''

def readHmStartTerms(text):
    s = text.split(' ')
    if s[0] == 'HMSTART':
        return {'hmdifIdCode': s[1],
                'hmdifVersionNo' : s[2],
                'textStartIdValue':s[3],
                'textEndIdValue':s[4],
            'recordEndTerm':s[5],
            'attrEndTerm' : s[6],
         'recordIdTerm' : s[7]}
        
def testreadHmStartTerms():
    line = 'HMSTART ukPMS 001 " " ; , \\'
    print(readHmStartTerms(line))


'''
    write HMSTART line
    terms dict -> str
'''
def writeHmStart(terms):
    #dict unordered for early python versions
    keys = ['hmdifIdCode','hmdifVersionNo','textStartIdValue','textEndIdValue','recordEndTerm',
     'attrEndTerm','recordIdTerm']
    return 'HMSTART ' + ' '.join([terms[k] for k in keys])


def testWriteHmStart():
    terms = {'hmdifIdCode': 'ukPMS', 'hmdifVersionNo': '001', 'textStartIdValue': '"', 
             'textEndIdValue': '"', 'recordEndTerm': ';', 'attrEndTerm': ',', 'recordIdTerm': '\\'}
    v = writeHmStart(terms)
    assert v == 'HMSTART ukPMS 001 " " ; , \\'


'''
str -> str
'TSTART;' -> 'TSTART'
'SURVEY\OWNER,TYPE,VERSION,NUMBER,SUBSECT,MACHINE,PREPROC,SVC,XSPUSED;' -> 'SURVEY'

'''
def lineType(line,terms):
    if terms['recordIdTerm'] in line:
        return line.split(terms['recordIdTerm'])[0]
    else:
        return line.split(terms['recordEndTerm'])[0]
    


def testLineType():
    terms = {'recordIdTerm':'\\','recordEndTerm':';'}
    r = lineType(r'SURVEY\OWNER,TYPE,VERSION,NUMBER,SUBSECT,MACHINE,PREPROC,SVC,XSPUSED;',terms)
    assert r=='SURVEY'
    
    r = lineType('TSTART;',terms) 
    #print(r)
    assert r == 'TSTART'
    
    r = lineType(r'TEND\7;',terms)
    print(r)
    assert r == 'TEND'

    
'''
    str -> []
'''    
def lineData(line,terms):
    #SURVEY\OWNER,TYPE,VERSION,NUMBER,SUBSECT,MACHINE,PREPROC,SVC,XSPUSED;
    line = line.strip()
    if line[-1] == terms['recordEndTerm']:
        line = line[:-1]
   # p = line.split(terms['recordIdTerm'])[1]
    #print('p',p)
    return line.split(terms['recordIdTerm'])[1].split(terms['attrEndTerm'])


def testLineData():
    terms = {'recordIdTerm':'\\','recordEndTerm':';','attrEndTerm':','}
    line = r'SURVEY\OWNER,TYPE,VERSION,NUMBER,SUBSECT,MACHINE,PREPROC,SVC,XSPUSED;'
    d = lineData(line,terms)
    print('d',d)


if __name__ in ('__main__','__console__'):
    #testLineType()
    testreadHmStartTerms()