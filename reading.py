# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 14:52:07 2024

@author: Drew.Bennett


todo:
    support tree?
    each line type has parent. line above it in template block.
    parent for data line should be last line of parent type.
    or type above it eg Blackburn 19-20_CL.HMD has no THRESHLD data lines
"""


'''
read start line like 'HMSTART ukPMS 001 " " ; , \\'
returns dict if sucessful
'''


import sys
import os

d = os.path.dirname(__file__)

if not d in sys.path:
    sys.path.append(d)


from template import template
from line_functions import lineType,readHmStartTerms



class hmdReadError(Exception):
    pass



        
'''
    read lines of file.
    returns HMSTART terms if found.
    leaves stream position at last read line.
'''

def readTerms(file,maxLine = 100):
    for line in file:
        line = line.strip()
        v = readHmStartTerms(line)
        if v:
            return v



'''
    returns dict of lineType:template.
    stream position needs to be before TSTART 
'''
def readTemplates(file,terms):
    started = False
    templates = {}
    for line in file:
        tp = lineType(line,terms)
       # print('line',line,'tp',tp)
        if started:
            if tp == 'TEND':
                return templates
            else:
                templates[tp] = template.fromLine(line = line , terms = terms)
        else:
            if tp == 'TSTART':
                started = True
            


'''
    class for reading hmd.
    iterate over instance to get data. 
    class rather than function because might want templates or terms.
'''

class hmdReader:
    #file:iterable filestream like
    def __init__(self,file):
        self.file = file
        self.terms = readTerms(file)
        if self.terms is None:
            raise hmdReadError('Could not read HMSTART line.')
        self.templates = readTemplates(file=file,terms = self.terms)
        if not self.templates:
            raise hmdReadError('Error reading template block.')
            
    # (lineType str,{field str:value str})        
    def __iter__(self):
        for line in self.file:
            tp = lineType(line,self.terms)
            if tp in self.templates:
                yield (tp,self.templates[tp].parseLine(line))
            