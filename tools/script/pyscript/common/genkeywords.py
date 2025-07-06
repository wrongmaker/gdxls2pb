#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.sax


class KeywrodsHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.id, self.mark, self.desc = '', '', ''
        self.contents = []
        self.enumContent = ''
        self.convKeys = {}

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        if tag == 'enum':
            self.id = attributes['id']
            self.mark = attributes['mark']
            self.desc = attributes['desc']
        elif tag == 'option':
            id = attributes['id']
            mark = attributes['mark']
            desc = attributes['desc']
            value = attributes['value']
            mark = self.mark + '-' + mark
            id = self.id.upper() + '_' + id.upper()
            self.convKeys[mark] = int(value)
            content = {
                'id': id,
                'mark': mark,
                'desc': desc,
                'value': value
            }
            self.contents.append(content)

    # 元素结束事件处理
    def endElement(self, tag):
        if tag == 'enum':
            protoEnumContent = '  {}_UNKNOWN = 0;\n'.format(self.id.upper())
            for content in self.contents:
                option = '  {} = {};  // {}\n'.format(
                    content['id'], content['value'], content['mark'])
                protoEnumContent += option
            protoEnum = 'enum {} {{  // {}\n{}}}\n\n'.format(
                self.id, self.desc, protoEnumContent)
            self.id, self.mark, self.desc = '', '', ''
            self.contents = []
            self.enumContent += protoEnum

    def serial(self, package):
        contentHead = 'syntax = "proto3";\n\npackage {};\n\n'.format(package)
        self.enumContent = contentHead + self.enumContent
        print(self.enumContent)
        return self.enumContent

    def getConvKeys(self):
        return self.convKeys


def __writeToFile(data, filePath):
    with open(filePath, 'wb') as file:
        file.write(data.encode('utf-8'))
        file.close()


def __getHandler(inFile):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    handler = KeywrodsHandler()
    parser.setContentHandler(handler)

    parser.parse(inFile)
    return handler


def GenKeywords(package, inFile, outFile):
    handler = __getHandler(inFile)
    content = handler.serial(package)
    __writeToFile(content, outFile)
    # print(handler.getConvKeys())


def GetConvKeys(inFile):
    handler = __getHandler(inFile)
    return handler.getConvKeys()


# if __name__ == '__main__':
#     GenKeywords('keywords.xml', 'keywords.proto')
