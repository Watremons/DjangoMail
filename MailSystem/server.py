import os

import json

import sys
sys.path.append(os.path.dirname(__file__))

from smtp import Smtp
from pop3 import Pop3


class Server:
    default = {
        'server': {'domain': 'test.com', 'mailMaxSize': 65565, 'logMaxSize': 65535},
        'smtp': {'port': 8025, 'logDir': '\\log\\smtp', 'banIPs': [], 'banActs': []},
        'pop3': {'port': 8110, 'logDir': '\\log\\pop3', 'banIPs': [], 'banActs': []}
    }

    def __init__(self, configs=default):
        self.state = 'stop'
        self.currConfigs = self.default
        self.ServerSetup(configs)
        self.path = os.path.abspath(os.path.dirname(__file__))

    def ServerSetup(self, configs):
        if configs is None:
            configs = self.default

        if self.state == 'stop':
            self.state = 'setup'
            self.currConfigs = configs
            serverConfig = configs['server']
            smtpConfig = configs['smtp']
            pop3Config = configs['pop3']
            self.domain = serverConfig['domain']
            self.mailMaxSize = serverConfig['mailMaxSize']
            self.logMaxSize = serverConfig['logMaxSize']
            self.logDir = [smtpConfig['logDir'], pop3Config['logDir']]

            self.smtp = Smtp(serverConfig['domain'], smtpConfig['port'], smtpConfig['logDir'], smtpConfig['banIPs'], smtpConfig['banActs'])
            self.pop3 = Pop3(pop3Config['port'], pop3Config['logDir'], pop3Config['banIPs'], pop3Config['banActs'], serverConfig['mailMaxSize'])

            print('server setup')
        else:
            print('server has been setup.')

    def ServerRun(self):
        self.state = 'run'
        self.smtp.start()
        self.pop3.start()
        print('server start running')

    def ServerShutdown(self):
        self.state = 'stop'
        self.smtp.stop()
        self.pop3.stop() 
        print('server shutdown')

    def ServerRestart(self):
        self.ServerShutdown()
        self.ServerSetup(self.currConfigs)

    def ConfigModify(self, configJson):
        newConfigs = self.currConfigs
        try:
            for server in newConfigs.keys():
                for config in newConfigs[server].keys():
                    newConfigs[server][config] = configJson[server][config]
            # for serverOld, serverNew in zip(newConfigs.values(), configJson.values()):
            #     for configOld, configNew in zip(serverOld.values(), serverNew.values()):
            #         configOld = configNew
        except:
            print('parameter error')
            return -1
        else:
            self.currConfigs = newConfigs
            filename = os.path.join(self.path, 'config.json')
            with open(filename, 'w', encoding='utf8') as f:
                configJson = json.dump(newConfigs, f)
            self.ServerShutdown()
            self.ServerSetup(self.currConfigs)
            return self.currConfigs

    def ConfigUpdate(self, serviceName, config, value):
        if serviceName == 'server':
            service = 0
        elif serviceName == 'smtp':
            service = 1
        elif serviceName == 'pop3':
            service = 2
        else:
            print('parameter error')
            return

        newConfigs = self.currConfigs
        try:
            if config in newConfigs[service].keys():
                newConfigs[service][config] = value
            else:
                print('parameter error')
                return
        except:
            print('parameter error')
            return
        else:
            self.currConfigs = newConfigs
            self.ServerShutdown()
            self.ServerSetup(self.currConfigs)

    def ConfigShow(self):
        try:
            filename = os.path.join(self.path, 'config.json')
            with open(filename, 'r', encoding='utf8') as f:
                configJson = json.load(f)
            return configJson

        except Exception as e:
            # logging.error('str(Exception):\t', str(Exception))
            # logging.error('str(e):\t\t', str(e))
            # logging.error('repr(e):\t', repr(e))
            # logging.error('########################################################')
            return -1

    def ConfigDefault(self):
        self.currConfigs = self.default
        print('the config set back to default')
        return self.currConfigs

    def ConfigSave(self, filename):
        filename = os.path.join(self.path, filename)
        try:
            with open(filename, 'w') as f:
                json.dump(self.currConfigs, f)
        except:
            print('save failed')

    def GetAllLogFile(self, type):
        if type != 0 and type != 1:
            print('parameter error')
            return

        overSize = False
        fileNames = []
        filePaths = []
        fileSizes = []
        allSize = 0
        dir = os.path.abspath(os.path.dirname(__file__)) + self.logDir[type]
        for root, dirs, files in os.walk(dir, topdown=False):
            for name in files:
                filepath = os.path.join(root, name)
                if overSize is True or name[-4:] != '.log':
                    os.remove(filepath)
                    continue

                size = os.path.getsize(filepath)
                if size + allSize > self.logMaxSize:
                    overSize = True
                    os.remove(filepath)
                else:
                    fileNames.append(name)
                    filePaths.append(filepath)
                    fileSizes.append(size)
                    allSize = allSize + size

        return fileNames, filePaths, fileSizes

    def ShowAllLogFile(self, type):
        fileNames, _, fileSizes = self.GetAllLogFile(type)
        print('log files ' + str(len(fileNames)))
        for i in range(len(fileNames)):
            print(str(i+1) + ' : ' + fileNames[i] + ' : ' + str(fileSizes[i]))

    def CheckLogFile(self, type, num):
        fileNames, filePaths, filesizes = self.GetAllLogFile(type)
        try:
            file = open(filePaths[num-1], 'r')
        except:
            print('parameter error')
            return
        else:
            print(fileNames[num-1], filesizes[num-1], 'bytes')
            content = file.read()
            print(content)

    def DelLogFile(self, type, num):
        fileNames, filePaths, filesizes = self.GetAllLogFile(type)
        try:
            os.remove(filePaths[num-1])
        except:
            print('parameter error')
            return
        else:
            print(fileNames[num-1], 'deleted')


def main():
    server = Server()
    # server.ConfigSave("config.json")
    server.ShowAllLogFile(0)


if __name__ == '__main__':
    main()
