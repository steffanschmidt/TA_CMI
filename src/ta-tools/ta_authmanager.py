#!/usr/bin/env python3
from __future__ import annotations
import requests

class AuthorizerTA:

    def __init__(self, userName: str = None, password: str = None):
        self.TASession = None
        self.TACRSFTokenStorageName = "csrf-token"
        self.TALoginURL = "https://cmi.ta.co.at/portal/checkLogin.inc.php"
        self.TALoginUserNameFieldName = "username"
        self.TALoginPasswordFieldName = "passwort"

        self.userCredentials = {}
        self.setCredentials(userName, password)

    def setUserName(self, userName: str = None):
        self.userName = userName

    def setPassword(self, password: str = None):
        self.password = password

    def setCredentials(self, userName: str = None, password: str = None):
        self.setUserName(userName)
        self.setPassword(password)

    def validateUserName(self) -> bool:
        return self.userName and isinstance(self.userName, str)

    def validatePassword(self) -> bool:
        return self.password and isinstance(self.password, str)

    def retreiveUserCredentials(self) -> dict:
        self.userCredentials = {}
        if self.validateUserName() and self.validatePassword():
            self.userCredentials = {
                self.TALoginUserNameFieldName: self.userName,
                self.TALoginPasswordFieldName: self.password
            }

        return self.userCredentials

    def setupSession(self) -> (bool, requests.sessions.Session, str):
        TASessionMsg = None
        TASessionStatus = False
        if not self.TASession:
            self.retreiveUserCredentials()
            if self.userCredentials:
                self.TASession = requests.Session()
                TASessionLoginResponse = self.TASession.post(self.TALoginURL, self.userCredentials)
                if TASessionLoginResponse.status_code == 200:
                    TASessionCookies = TASessionLoginResponse.cookies
                    TASessionCRSFToken = TASessionCookies[self.TACRSFTokenStorageName] if self.TACRSFTokenStorageName in TASessionCookies else None
                    if TASessionCRSFToken:
                        self.TASession.headers["authorization"] = TASessionCRSFToken
                        TASessionStatus = True
                    else:
                        self.closeSession()
                else:
                    self.closeSession()
            else:
                self.TASession = None

        return TASessionStatus, self.TASession, TASessionMsg

    def closeSession(self):
        if self.TASession:
            self.TASession.close()
            self.TASession = None

if __name__ == "__main__":
    AuthorizerTA = AuthorizerTA()