# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:52:58 2024

@author: Drew.Bennett
"""


from template import template
from line_functions import writeHmStart





'''
    file: filestream like
    data: iterable of (lineType,{fieldName:value})
'''
def writeHmd(file,data,terms,templates):
    lineCount = 1
    
    def writeLine(text):
        file.write('\n'+text)
        nonlocal lineCount
        lineCount += 1
           
    #template block
    file.write(writeHmStart(terms))
    writeLine('TSTART'+terms['recordEndTerm'])
    for key,t in templates.items():
        writeLine(t.writeTemplateLine())
    writeLine('TEND' + terms['recordIdTerm'] + str(len(templates) + 2) + terms['recordEndTerm'])
    writeLine('DSTART' + terms['recordEndTerm'])

    dataCount = 0
    for d in data:
        file.write('\n' + templates[d[0]].writeLine(d[1]))
        dataCount += 1
        lineCount += 1
        
    writeLine('DEND' + terms['recordIdTerm'] + str(dataCount+2) + terms['recordEndTerm'])#includes DSTART and DEND

    file.write('\nHMEND' + terms['recordIdTerm'] + str(lineCount+1) + terms['recordEndTerm'])

    
def testWriteHmd():
    terms = {'hmdifIdCode': 'ukPMS', 'hmdifVersionNo': '001', 'textStartIdValue': '"', 
             'textEndIdValue': '"', 'recordEndTerm': ';', 'attrEndTerm': ',', 'recordIdTerm': '\\'}
    templates = {}
    templates['SURVEY'] = template.fromLine(r'SURVEY\OWNER,TYPE,VERSION,NUMBER,SUBSECT,MACHINE,PREPROC,SVC,XSPUSED;',terms)
    templates['SECTION'] = template.fromLine(r'SECTION\NETWORK,LABEL,SNODE,LENGTH,SDATE,EDATE,STIME,ETIME;',terms)
    templates['THRESHLD'] = template.fromLine(r'THRESHLD\FTXSECT,FTSCHAIN,FTECHAIN,FTSDATE,FTNUM,PIFIND,SCODE;',terms)
    templates['OBSERV'] = template.fromLine(r'OBSERV\DEFECT,VERSION,XSECT,SCHAIN,ECHAIN;',terms)
    templates['OBVAL'] = template.fromLine(r'OBVAL\PARM,OPTION,VALUE,PERCENT;',terms)
  
    data = [('SURVEY', {'OWNER': 'UKPMS', 'TYPE': 'SCRIM', 'VERSION': '', 'NUMBER': '5', 'SUBSECT': '10M', 'MACHINE': 'HSL', 'PREPROC': 'V0116a', 'SVC': '1', 'XSPUSED': ' F'})]
    
    with open('test_output.hmd','w') as f:
        writeHmd(file = f,data = data , terms = terms,templates = templates)


if __name__ in ('__main__','__console__'):
    testWriteHmd()