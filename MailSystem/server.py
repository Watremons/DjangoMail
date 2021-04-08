'''
@Author: One_Random
@Date: 2020-04-13 17:21:23
@LastEditors: One_Random
@LastEditTime: 2020-05-26 18:05:14
@FilePath: /mail/server.py
@Description: Copyright © 2020 One_Random. All rights reserved.
'''

import os
import sys

import json

from user import *
from smtp import Smtp
from pop3 import Pop3


class Server:
    default = [{'domain': 'test.com', 'mailMaxSize': 65565, 'logMaxSize': 65535}, {'port': 8025, 'logDir': '/log/smtp', 'banIPs': [], 'banActs': []}, {'port': 8110, 'logDir': '/log/pop3', 'banIPs': [], 'banActs': []}]

    def __init__(self, configs=default):
        self.state = 'stop'
        self.currConfigs = self.default
        self.server_setup(configs)

    def server_setup(self, configs):
        if configs == None:
            configs = self.default
            
        if self.state == 'stop':
            self.state = 'setup'
            self.currConfigs = configs
            server_config = configs[0]
            smtp_config = configs[1]
            pop3_config = configs[2]
            self.domain = server_config['domain']
            self.mailMaxSize = server_config['mailMaxSize']
            self.logMaxSize = server_config['logMaxSize']
            self.logDir = [smtp_config['logDir'], pop3_config['logDir']] 

            self.smtp = Smtp(server_config['domain'], smtp_config['port'], smtp_config['logDir'], smtp_config['banIPs'], smtp_config['banActs'])
            self.pop3 = Pop3(pop3_config['port'], pop3_config['logDir'], pop3_config['banIPs'], pop3_config['banActs'], server_config['mailMaxSize'])

            print('server setup')
        else:
            print('server has been setup.')

    def server_run(self):
        self.state = 'run'
        self.smtp.start()
        self.pop3.start()
        print('server start running')

    def server_shutdown(self):
        self.state = 'stop'
        self.smtp.stop()
        self.pop3.stop()
        print('server shutdown')

    def server_restart(self):
        self.server_shutdown()
        self.server_setup(self.currConfigs)

    def config_update(self, serviceName, config, value):
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
            self.server_shutdown()
            self.server_setup(self.currConfigs)
        
    def config_show(self):
        print(self.currConfigs)

    def config_default(self):
        self.currConfigs = self.default
        print('the config set back to default')

    def config_save(self, filename):
        filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
        try:
            with open(filename, 'w') as f:
                json.dump(self.currConfigs, f)
        except:
            print('save failed')

    def getAllLogFile(self, type):
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
                if overSize == True or name[-4:] != '.log':
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

    def showAllLogFile(self, type):
        fileNames, _, fileSizes = self.getAllLogFile(type)
        print('log files ' + str(len(fileNames)))
        for i in range(len(fileNames)):
            print(str(i+1) + ' : ' + fileNames[i] + ' : ' + str(fileSizes[i]))

    def checkLogFile(self, type, num):
        fileNames, filePaths, filesizes = self.getAllLogFile(type)
        try:
            file = open(filePaths[num-1], 'r')
        except:
            print('parameter error')
            return
        else:
            print(fileNames[num-1], filesizes[num], 'bytes')
            content = file.read()
            print(content)

    def delLogFile(self, type, num):
        fileNames, filePaths, filesizes = self.getAllLogFile(type)
        try:
            os.remove(filePaths[num-1])
        except:
            print('parameter error')
            return
        else:
            print(fileNames[num-1], 'deleted')

def main():
    server = Server()
    # server.config_save("config.json")
    server.showAllLogFile(0)

if __name__ == '__main__':
    main()