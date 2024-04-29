# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 09:23:15 2024

@author: Drew.Bennett
"""

#import parse
from line_functions import lineData,lineType,readHmStartTerms
import io

class template:
    
    def __init__(self,terms,recordType = '',fieldNames = [],outputTemplate = ''):
        self.terms = terms
        self.fieldNames = fieldNames
        self.outputTemplate = outputTemplate
        self.recordType = recordType


    #write line of file
    def writeLine(self,data):
        if isinstance(data,dict):
            return self.outputTemplate.format(**data)
        else:
            return self.outputTemplate.format(**self.toDict(data))
    
    
    #->str
    def writeTemplateLine(self):
        return self.recordType + self.terms['recordIdTerm'] + self.terms['attrEndTerm'].join(self.fieldNames) + self.terms['recordEndTerm']
    
    
    #iterable to dict of fieldname:value. assuming same order
    def toDict(self,it):
        return dict(zip(self.fieldNames,it))
         
    
    
    '''
    read line of file
    returns [str].
    ignores field lengths and uses attrEndTerm
    '''
    def parseLine(self,text):
        data = lineData(line=text , terms = self.terms)
       # print('data',data)
        return self.toDict(data)




   
    '''
    template from terms and line of file template block
    '''
    @staticmethod
    def fromLine(line,terms):
        line = line.strip()
        fieldNames = lineData(line=line , terms = terms)
        outputTemplate = line
        for f in fieldNames:
            outputTemplate = outputTemplate.replace(f,'{' + f + '}')
        return template(terms = terms ,
                        fieldNames = fieldNames ,
                        outputTemplate = outputTemplate,
                        recordType = lineType(line,terms))
            


if __name__ in ('__console__','__main__'):
    terms = {'recordIdTerm':'\\','recordEndTerm':';','attrEndTerm':','}
    templateLine = r'SURVEY\OWNER,TYPE,VERSION,NUMBER,SUBSECT,MACHINE,PREPROC,SVC,XSPUSED;'
    t = template.fromLine(terms = terms , line = templateLine)
    line = r'SURVEY\UKPMS,SCRIM,,5,10M,HSL,V0116a,1, F;'
    r = t.parseLine(line)
    print(r)
    newLine = t.writeLine(r)
    print('newLine',newLine)
    assert newLine == line
    
    