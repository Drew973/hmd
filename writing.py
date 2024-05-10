# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:52:58 2024

@author: Drew.Bennett
"""


from template import template
from line_functions import writeHmStart

from io import StringIO
from reading import hmdReader

'''
    file: filestream like
    data: iterable of (lineType,{fieldName:value})
'''


class hmdWriter:

    def __init__(self, templates, terms, file):
        self.templates = templates
        self.terms = terms
        self.file = file
        self.lineCount = 0
        self.dataCount = 0

    def writeLine(self, text):
        self.lineCount += 1
        self.file.write(text+'\n')

    def writeDataLine(self, lineType, data):
        self.writeLine(self.templates[lineType].writeLine(data))
        self.dataCount += 1

    # data is iterable of (lineType,{})
    def writeFile(self, data):
        # start block
        self.writeLine(writeHmStart(self.terms))
        self.writeLine('TSTART'+self.terms['recordEndTerm'])
        for key, t in self.templates.items():
            self.writeLine(t.writeTemplateLine())
        self.writeLine('TEND' + self.terms['recordIdTerm'] + str(len(
            self.templates) + 2) + self.terms['recordEndTerm'])  # count includes TStart and TEND

        self.writeLine('DSTART' + self.terms['recordEndTerm'])

        for d in data:
            self.writeDataLine(lineType=d[0], data=d[1])

        self.writeLine('DEND' + self.terms['recordIdTerm'] + str(
            self.dataCount+2) + self.terms['recordEndTerm'])  # count includes DSTART and DEND
        self.writeLine('HMEND' + self.terms['recordIdTerm'] +
                       str(self.lineCount+1) + self.terms['recordEndTerm'])


    @staticmethod
    def fromTemplateBlock(templateBlock, file):
        if isinstance(templateBlock, str):
            templateBlock = StringIO(templateBlock)
        reader = hmdReader(templateBlock)
        return hmdWriter.fromReader(reader = reader, file=file)


    @staticmethod
    def fromReader(file,reader):
        return hmdWriter(templates=reader.templates, terms=reader.terms, file=file)


def testWriter():
    data = [('SURVEY', {'OWNER': 'UKPMS', 'TYPE': 'SCRIM', 'VERSION': '', 'NUMBER': '5',
             'SUBSECT': '10M', 'MACHINE': 'HSL', 'PREPROC': 'V0116a', 'SVC': '1', 'XSPUSED': ' F'})]

    templateBlock = r'''HMSTART ukPMS 001 " " ; , \
TSTART;
SURVEY\OWNER,TYPE,VERSION,NUMBER,SUBSECT,MACHINE,PREPROC,SVC,XSPUSED;
SECTION\NETWORK,LABEL,SNODE,LENGTH,SDATE,EDATE,STIME,ETIME;
THRESHLD\FTXSECT,FTSCHAIN,FTECHAIN,FTSDATE,FTNUM,PIFIND,SCODE;
OBSERV\DEFECT,VERSION,XSECT,SCHAIN,ECHAIN;
OBVAL\PARM,OPTION,VALUE,PERCENT;
TEND\7;
    '''


    with open('test_output.hmd', 'w') as f:
        w = hmdWriter.fromTemplateBlock(templateBlock = templateBlock, file = f)
        w.writeFile(data=data)


if __name__ in ('__main__', '__console__'):
    testWriter()
