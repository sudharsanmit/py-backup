import logging
import logging.config
import hi
import configparser
import os
import sys

cfgparser = configparser.SafeConfigParser()
cfgparser.optionxform = str

def getDirName():
    try:
        dirname = os.path.dirname(os.path.abspath(__file__))
    except NameError:  
        dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
    return dirname

def getAbsPath(fileName):
    return os.path.join(getDirName(),fileName)

def getConfig():
    return cfgparser 

def loadConfig(fileName):
    cfgparser.readfp(open(getAbsPath(fileName)))

def getConfigElement(section,key):
    return getConfig().get(section,key)

def main():
    loadConfig('config/logging.conf')
    print(getConfig().get('loggers','keys'))
    print(getConfigElement('loggers','keys'))

    print (cfgparser.get('loggers','keys'))

    

if __name__ == '__main__':
    main()


