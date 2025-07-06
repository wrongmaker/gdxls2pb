import os


def __scanFile(basePathLen, path, fileList):
    newPath = path
    if os.path.isfile(path):
        if path.endswith('.proto'):
            fileLen = len(os.path.basename(path))
            fileList.append([path[-fileLen:], path[basePathLen:-fileLen]])
    elif os.path.isdir(path):
        for s in os.listdir(path):
            newPath = os.path.join(path, s)
            __scanFile(basePathLen, newPath, fileList)
    return fileList


def __checkAndMkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def __genProto(protocPath, scanBasePath, genOutPath, list, includes, genType, desc):
    istr = ''
    for i in includes:
        istr += ' -I' + i
    for one in list:
        file, protoFile = one
        genOut = genOutPath
        __checkAndMkdir(genOut)
        realFile = protoFile + file
        descOut = ''
        if desc:
            descDir = genOut + '/desc/' + protoFile
            __checkAndMkdir(descDir)
            descOut = ' --descriptor_set_out=' + descDir + file + '.desc '
        cmd = 'cd ' + scanBasePath + ' && '
        cmd += protocPath + descOut + ' --' + genType + \
            '=' + genOut + ' ' + realFile + istr
        os.system(cmd)
        print(cmd)


def GenAsPython(protocPath, scanBasePath, scanPath, genOutPath, includes):
    basePathLen = len(scanBasePath)
    list = __scanFile(basePathLen, scanPath, [])
    __genProto(protocPath, scanBasePath, genOutPath,
               list, includes, 'python_out', False)
