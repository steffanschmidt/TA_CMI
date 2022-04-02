#!/usr/bin/env python3
import requests

class AuthorizerTA:

    def __init__(self, userName: None, password: None):
        self.TASession = None

        self.TACRSFTokenStorageName = "csrf-token"
        self.TALoginURL = "https://cmi.ta.co.at/portal/checkLogin.inc.php"
        self.TALoginUserNameFieldName = "username"
        self.TALoginPasswordFieldName = "passwort"
        
        self.userCredentials = {}

        self.setUserName(setUserName)
        self.setPassword(password)

    def setUserName(self, userName: str = None):
        self.userName = userName

    def setPassword(self, password: str = None):
        self.password = password

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

    def setupTASession(self) -> requests.sessions.Session:
        if not self.TASession:
            self.retreiveUserCredentials()
            if self.retreiveCredentials:
                self.TASession = requests.Session()
                self.TASessionLoginResponse = self.TASession.post(self.TALoginURL, self.userCredentials)
                if self.TASessionLoginResponse.status_code == "200":
                    
                else:
                    self.closeTASession()
            else:
                self.TASession = None

        return self.TASession

    def closeTASession(self):
        if self.TASession:
            self.TASession.close()
            self.TASession = None

if __name__ == "__main__":
    pass