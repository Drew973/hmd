# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 10:57:34 2024

@author: Drew.Bennett
"""


import sys
import os

d = os.path.dirname(os.path.dirname(__file__))

if not d in sys.path:
    sys.path.append(d)


from reading import hmdReader
from writing import hmdWriter


def testFile(file):
    with open(file,'r') as f:
        reader = hmdReader(f)
        outFile = os.path.splitext(file)[0] + '_out.hmd'
        with open(outFile,'w') as f2:
            w = hmdWriter.fromReader(file = f2,reader = reader)
            w.writeFile(data = reader)
    with open(file,'r') as f:
        inputText = f.read().strip()
    with open(outFile,'r') as f2:
        outputText = f2.read().strip()
    assert inputText == outputText
    

if __name__ in ('__main__','__console__'):
    '''integration test.
    reads hmd and writes data to different file. Checks new file is same as original.
    '''
    testFile('Blackburn 19-20_CL.HMD')
    testFile('Blackburn 19-20_CR.HMD')
    
  
    