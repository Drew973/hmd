# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 10:57:34 2024

@author: Drew.Bennett
"""


import sys
import os
import io

d = os.path.dirname(os.path.dirname(__file__))

if not d in sys.path:
    sys.path.append(d)


from reading import hmdReader,readTerms,readTemplates
from writing import writeHmd


if __name__ in ('__main__','__console__'):
    '''integration test.
    reads hmd and writes data to different file. Checks new file is same as original.
    '''
    #testReadHmStart()
    file = 'Blackburn 19-20_CL.HMD'
    with open(file,'r') as f:
        reader = hmdReader(f)
        outFile = 'Blackburn 19-20_CL_out.HMD'
        with open(outFile,'w') as f2:
            writeHmd(file = f2,data = reader,templates = reader.templates,terms = reader.terms)
    with open(file,'r') as f:
        inputText = f.read()
    with open(outFile,'r') as f2:
        outputText = f2.read()
    assert inputText == outputText
    