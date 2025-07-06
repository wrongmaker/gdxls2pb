import os

TOOLS_PATH = os.getcwd() + '/../../../'
PROTOC_ENV_WIN = TOOLS_PATH + '/tools/protoc/windows/bin/protoc.exe'

def GetToolsPath():
  return TOOLS_PATH

def GetProtocEnvPath():
  return PROTOC_ENV_WIN

