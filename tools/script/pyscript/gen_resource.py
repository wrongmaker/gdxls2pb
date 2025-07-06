from common import genproto
from common import genpbin
from common import genkeywords
from pyenv import GetToolsPath, GetProtocEnvPath

basePath = GetToolsPath()
excelPath = basePath + 'resource/excel/'
keywordsPath = excelPath + 'xml/keywords.xml'
scanPath = excelPath + 'proto/'
exportPath = excelPath + 'export/'
xlsPath = excelPath + 'xls/'
includePath = []

if __name__ == '__main__':
    genproto.GenProto(xlsPath, scanPath)
    convKeys = genkeywords.GetConvKeys(keywordsPath)
    genpbin.GenPbin(convKeys, GetProtocEnvPath(), scanPath,
                    scanPath, xlsPath, exportPath, includePath)
