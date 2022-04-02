#!/usr/bin/env python3

class MySQLBaseWorker:

    def __init__(self):
        self.taMySQLConnector = None
        self.taMySQLCursor = None

    def setMySQLUserName(self, mysqlUserName: str = None):
        self.mysqlUserName = mysqlUserName

    def setMySQLPassword(self, mysqlPassword: str = None):
        self.mysqlPassword = mysqlPassword

    def setMySQLCredentials(self, mysqlUserName: str = None, mysqlPassword: str = None):
        self.setMySQLUserName(mysqlUserName)
        self.setMySQLPassword(mysqlPassword)

    def setupMySQLConnection(self):
        pass

    def closeMySQLConnection(self):
        pass

    def executateMySQLQuery(self, query: str = None, params = []):
        pass