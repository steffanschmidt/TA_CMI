#!/usr/bin/env python3
from __future__ import annotations
import sys, re
import pandas as pd
import datetime as dt
from bs4 import BeautifulSoup
from pathlib import Path
sys.path.insert(1, f"{Path(__file__).parent}/../auth")
from ta_authmanager import AuthorizerTA

class DataRetrieverTA(AuthorizerTA):

    def __init__(self, userName: str = None, password: str = None):
        super().__init__(userName, password)
        # General Information
        self.requestTimeoutTime = 5
        
        # TA Profile and CMI Information - This is display under the tab Overview
        self.TAPortalOverviewURL = "https://cmi.ta.co.at/portal/ta/overview/"
        self.TAPortalOverviewContents = None
        self.TAOtherCMIDivId = "otherCMIs"
        self.TAOwnCMIDivId = "myCMIs"

        # TA CMI Information
        self.TADevicesURL = "https://cmi.ta.co.at/portal/geraete/getDevice.php"
        self.TADeviceModeFieldName = "mode"
        self.TADeviceOrderDirFieldName = "asc"
        self.TADeviceOrderColFieldName = "order_column"
        self.TADeviceSearchValueFieldName = "search_value"
        self.TADeviceStartFieldName = "start"
        self.TAOwnDevicesRequest = {
            self.TADeviceModeFieldName: 1,
            self.TADeviceOrderDirFieldName: "asc",
            self.TADeviceOrderColFieldName: 0,
            self.TADeviceSearchValueFieldName: "",
            self.TADeviceStartFieldName: 0
        }
        self.TAOtherDevicesRequest = {**self.TAOwnDevicesRequest}
        self.TAOtherDevicesRequest[self.TADeviceModeFieldName] = 0

        self.TACMIDataKeyName = "data"
        self.CMIDataIdFieldName = "id"
        self.TAOwnCMIOptions = []
        self.TAOwnCMIOptionIDs = []
        self.TAOtherCMIOptions = []
        self.TAOtherCMIOptionIDs = []
        self.TAAllCMIOptions = []
        self.TAAllCMIOptionIDs = []

        # TA CMI Data Profiles Information
        self.CMIProfilesURL = "https://cmi.ta.co.at/portal/visual/getprofiledata.php"
        self.TADataProfiles = {}

        # TA User Name Information - This is display under the tab Account management
        self.assumeTAUserNameIsUserName = True
        self.TAUserName = None
        self.TAUserNameFieldIDName = "login"
        self.TAUserAccountManagementURL = "https://cmi.ta.co.at/portal/ta/konto/"

        # TA Data Analog/Digital Request Information
        self.TADataRequestURL = "https://cmi.ta.co.at/portal/visual/getlogdata.php"
        self.TAStatusHeader = "status"
        self.TAStatusSuccessName = "success"
        self.TAStatusFailedName = "fail"
        self.TADataHeader = "data"
        self.TADataUnitsInformationHeader = "units"
        self.TADataUnitHeader = "unity"
        self.TADataDescriptionHeader = "description"
        self.TADataColourHeader = "colour"
        self.TADataFactorHeader = "factor"
        self.TADataSensorReadingsHeader = "val"
        self.TADataSensorReadingTimeHeader = "zeit"
        self.validRequestModes = [
            "digital",
            "analog"
        ]
        self.TACMIFieldName = "cmi"
        self.TAFromFieldName = "from"
        self.TAToFieldName = "to"
        self.TAModeFieldName = "mode"
        self.TACreatorFieldName = "creator"
        self.TAProfileFieldName = "profil"
        self.dateFormat = "%Y-%m-%d"
        self.TADateTimeRequestFormat = f"{self.dateFormat} %H:%M:%S"
        self.defaultTARequestDays = 1

        # Used for collecting data into a Dataframe
        self.dataMeasurementTime = "Time"
        self.dataSensorIDHeader = "SensorID"
        self.dataSensorNameHeader = "SensorName"
        self.dataTypeHeader = "Type"
        self.dataValueHeader = "Value"
        self.dataUnitHeader = "Unit"

        self.TADataCollectorHeaders = [
            self.dataMeasurementTime,
            self.dataSensorIDHeader,
            self.dataSensorNameHeader,
            self.dataTypeHeader,
            self.dataValueHeader,
            self.dataUnitHeader
        ]


    """

    """
    def convertDateTimeToString(self, dateTime: dt.datetime = None) -> str:
        dateTimeString = None
        if isinstance(dateTime, (dt.date, dt.datetime)):
            try:
                dateTimeString = dt.datetime.strftime(dateTime, self.TADateTimeRequestFormat)
            except:
                dateTimeString = None
    
        if not isinstance(dateTimeString, str):
            dateTimeString = None

        return dateTimeString

    """

    """
    def convertStringToDateTime(self, dateTimeString: str = None) -> dt.datetime:
        dateTime = None
        if isinstance(dateTimeString, str):
            try:
                dateTime = dt.datetime.strptime(dateTimeString, self.TADateTimeRequestFormat)
            except:
                dateFormattedTime = dt.datetime.strptime(dateTimeString, self.dateFormat)
            finally:
                dateTime = None
        elif isinstance(dateTimeString, dt.datetime):
            dateTime = dateTimeString
        elif isinstance(dateTimeString, dt.date):
            dateTimeString = self.convertDateTimeToString(dateTimeString)
            dateTime = dt.datetime.strptime(dateTimeString, self.TADateRequestFormat)

        if dateTime and not isinstance(dateTime, dt.datetime):
            dateTime = None

        return dateTime

    """

    """
    def retrieveOwnCMIOptions(self, refreshCMIs: bool = False, keepSessionOpen: bool = False):
        if not self.TAOwnCMIOptions or refreshCMIs:
            ownDeviceRequestResponse = self.executeTAGetRequest(self.TADevicesURL, self.TAOwnDevicesRequest, keepSessionOpen)
            ownDeviceRequestResponseStatus = ownDeviceRequestResponse[0]
            ownDeviceRequestResponseData = ownDeviceRequestResponse[1].json() if ownDeviceRequestResponseStatus else {}
            if self.TACMIDataKeyName in ownDeviceRequestResponseData:
                self.TAOwnCMIOptions = ownDeviceRequestResponseData[self.TACMIDataKeyName]
            else:
                self.TAOwnCMIOptions = []

        self.TAOwnCMIOptionIDs = [CMIOptionData[self.CMIDataIdFieldName] for CMIOptionData in self.TAOwnCMIOptions]
        if not keepSessionOpen:
            self.closeSession()

        return self.TAOwnCMIOptions

    """

    """
    def retrieveOwnCMINames(self, refreshCMIs: bool = False, keepSessionOpen: bool = False) -> list[str]:
        self.retrieveOwnCMIOptions(refreshCMIs, keepSessionOpen)
        return self.TAOwnCMIOptionIDs

    """

    """
    def retrieveOtherCMIOptions(self, refreshCMIs: bool = False, keepSessionOpen: bool = False) -> list[dict]:
        if not self.TAOtherCMIOptions or refreshCMIs:
            otherDeviceRequestResponse = self.executeTAGetRequest(self.TADevicesURL, self.TAOtherDevicesRequest, keepSessionOpen)
            otherDeviceRequestResponseStatus = otherDeviceRequestResponse[0]
            otherDeviceRequestResponseData = otherDeviceRequestResponse[1].json() if otherDeviceRequestResponseStatus else {}
            if self.TACMIDataKeyName in otherDeviceRequestResponseData:
                self.TAOtherCMIOptions = otherDeviceRequestResponseData[self.TACMIDataKeyName]
            else:
                self.TAOtherCMIOptions = []

        self.TAOtherCMIOptionIDs = [CMIOptionData[self.CMIDataIdFieldName] for CMIOptionData in self.TAOtherCMIOptions]
        if not keepSessionOpen:
            self.closeSession()

        return self.TAOtherCMIOptions

    """

    """
    def retrieveOtherCMIOptionIDs(self, refreshCMIs: bool = False, keepSessionOpen: bool = False) -> list[str]:
        self.retrieveOtherCMIOptions(refreshCMIs, keepSessionOpen)
        return self.TAOtherCMIOptionIDs

    """

    """
    def retrieveCMIOptions(self, refreshCMIs: bool = False, keepSessionOpen: bool = False) -> list[dict]:
        self.retrieveOwnCMIOptions(refreshCMIs, True)
        self.retrieveOtherCMIOptions(refreshCMIs, True)
        self.TAAllCMIOptions = [*self.TAOwnCMIOptions, *self.TAOtherCMIOptions]
        self.TAAllCMIOptionIDs = [*self.TAOwnCMIOptionIDs, *self.TAOtherCMIOptionIDs]
        if not keepSessionOpen:
            self.closeSession()

        return self.TAAllCMIOptions

    """

    """
    def retrieveCMIOptionIDs(self, refreshCMIs: bool = False, keepSessionOpen: bool = False) -> list[str]:
        self.retrieveCMIOptions(refreshCMIs, keepSessionOpen)
        return self.TAAllCMIOptionIDs

    """
        Retrieves all the CMI IDs (both own CMIs and other CMIs) and creates a list of the valid CMI names
        If the CMI Name is found within this list, then it is valid. This flag 'refreshCMIs' can be used
        to force a refresh of this list. Otherwise if any are stored it will use those rather than
        fetching the CMI IDs again.
    """
    def validateCMIName(self, CMIName: str = None, refreshCMIs: bool = False) -> bool:
        validCMIName = False
        if CMIName and isinstance(CMIName, str):
            self.retrieveCMIOptionIDs()
            validCMIName = CMIName.upper() in self.TAAllCMIOptionIDs

        return validCMIName

    """
        Retrieves the TA user name. If this is not the same as the user name provided upon entry,
        then 'assumeTAUserNameIsUserName' can be set to False and retrieved directly from Account Management.
    """
    def retrieveTAUserName(self, refreshUserName: bool = False, keepSessionOpen: bool = False) -> str:
        if self.assumeTAUserNameIsUserName:
            self.TAUserName = self.userName.lower() if isinstance(self.userName, str) else None
        
        if not self.TAUserName or refreshUserName:
            openedTAUserNameSession = False
            if not self.TASession:
                openedTAUserNameSession = True
                self.setupSession()

            if self.TASession:
                TAUserAccountResponse = self.TASession.get(self.TAUserAccountManagementURL)
                TAUserAccountParsedData = BeautifulSoup(TAUserAccountResponse.text, "html.parser")
                TAUserAccountNameInformation = TAUserAccountParsedData.find("input", {"id": self.TAUserNameFieldIDName})
                if TAUserAccountNameInformation is not None:
                    self.TAUserName = TAUserAccountNameInformation.get("value")

            if not keepSessionOpen and openedTAUserNameSession:
                self.closeSession()

        return self.TAUserName

    """
        Validate the CMI Name by finding all CMI names. If the CMI name is valid the profiles are retrieved.
        If the CMI profiles have been found before, it returns those unless 'refreshProfiles' is set to True.
        In that case it retrieves the CMI profiles and update the profiles dictionary with the newly found
        profile.
        If the CMI names is invalid an empty list is returned
    """
    def retrieveCMIProfiles(self, CMIName: str = None, refreshProfiles: bool = False) -> list[str]:
        if self.validateCMIName(CMIName):
            if CMIName not in self.TADataProfiles or refreshProfiles:
                CMIName = CMIName.upper()
                CMIProfilesResponse = self.executeTAGetRequest(f"https://cmi.ta.co.at/portal/ta/visual/{CMIName}")
                CMIProfilesStatus = CMIProfilesResponse[0]
                CMIProfilesSiteContents = CMIProfilesResponse[1].text
                CMIProfilesSiteParsed = BeautifulSoup(CMIProfilesSiteContents, "html.parser")
                CMIProfilesSelector = CMIProfilesSiteParsed.find("select", {"id": "sel_profil"})
                CMIProfileOptions = CMIProfilesSelector.find_all("option")
                CMIProfileOptionNames = [CMIProfileOption.get("name") for CMIProfileOption in CMIProfileOptions]
                self.TADataProfiles[CMIName] = CMIProfileOptionNames

        CMIProfiles = self.TADataProfiles[CMIName] if CMIName in self.TADataProfiles else []
        return CMIProfiles
    
    """
        Validate the CMI Profile Name. This is case insensitive. If the CMI name is invalid an
        empty
    """
    def validateProfile(self, CMIName: str = None, profileName: str = None) -> bool:
        profileValid = False
        if profileName and isinstance(profileName, str):
            CMIProfiles = self.retrieveCMIProfiles(CMIName)
            profileName = profileName.lower()
            CMIProfilesLowered = [CMIProfile.lower() for CMIProfile in CMIProfiles]
            profileValid = profileName in CMIProfilesLowered
        
        return profileValid

    def validateRequestMode(self, requestMode: str = None):
        return requestMode and isinstance(requestMode, str) and requestMode.lower() in self.validRequestModes

    def composeTADataRequest(self, CMIName: str = None, profileName: str = None, requestMode: str = None, fromDate: None = str, toDate: None = str) -> (bool, dict, str):
        baseDataRequest = {}
        baseDataRequestMessage = None
        baseDataRequestStatus = False
        if self.validateRequestMode(requestMode):
            requestMode = requestMode.lower()
            if self.validateCMIName(CMIName):
                CMIName = CMIName.upper()
                profileNameValid = self.validateProfile(CMIName, profileName)
                if profileNameValid:
                    self.retrieveTAUserName()
                    if not fromDate and not toDate:
                        toDate = dt.datetime.now().replace(microsecond = 0)
                        fromDate = toDate - dt.timedelta(days = self.defaultTARequestDays)
                    elif not fromDate:
                        toDate = self.convertStringToDateTime(toDate)
                        fromDate = toDate - dt.timedelta(days = self.defaultTARequestDays) if toDate else None
                    elif not toDate:
                        toDate = dt.datetime.now()

                    sanitizedFromDate = self.convertDateTimeToString(fromDate)
                    sanitizedToDate = self.convertDateTimeToString(toDate)
                    if sanitizedFromDate and sanitizedToDate:
                        baseDataRequest = {
                            self.TACMIFieldName: CMIName,
                            self.TAFromFieldName: sanitizedFromDate,
                            self.TAToFieldName: sanitizedToDate,
                            self.TAModeFieldName: requestMode,
                            self.TACreatorFieldName: self.TAUserName,
                            self.TAProfileFieldName: profileName,
                            "_": dt.datetime.now().timestamp() * 1000
                        }
                        baseDataRequestStatus = True
                    else:
                        if not sanitizedFromDate and not sanitizedToDate:
                            baseDataRequestMessage = f"Missing both the from and to date. Please control your format (Provided: From = {fromDate}, To = {toDate})"
                        elif not sanitizedFromDate:
                            baseDataRequestMessage = f"Missing from date. Please control your format (Provided: From = {fromDate}"
                        else:
                            baseDataRequestMessage = f"Missing to date. Please control your format (Provided: From = {toDate}"
                else:
                    baseDataRequestMessage = f"Invalid Profile Name (Provided: {profileName}). Make sure the profile exists or control your spelling."
            else:
                baseDataRequestMessage = "Missing CMI Name"
        else:
            baseDataRequestMessage = f"Invalid Request Mode (Provided {requestMode}). Only {', '.join(self.validRequestModes)} allowed"

        return baseDataRequestStatus, baseDataRequest, baseDataRequestMessage

    """
        Extract the analog or digital information and places it into a dataframe. The request returns a dictionary with a 'status'
        and 'data' is returned. If the 'status' is a success, it will have the value 'success'. Otherwise it will have value 'fail'.
        In case of the failure, the data container contains the error message. Otheriwse it will be a dict with the following keys:
            - 'description' => The sensor names
            - 'units' => The unit of the sensor reading (dict containing:
                'unity' = The unit,
                'decimal' = The amount of decimals to be display
                'index' = A number
            )
            - 'colour' => Determines the line color in the webportal, User set property
            - 'factor' => used to emphasize certain sensor by multiplying with the set factor, User set property
            - 'val' => The actual sensor value, contains 'zeit/time' and the values for the sensor
    """
    def extractTADataResponseInformation(self, TADataRequestInformation: dict = {}) -> (bool, pd.DataFrame, str):
        TADataResponseStatus = False
        TADataResponseDataCollector = {TADataCollectorHeader: [] for TADataCollectorHeader in self.TADataCollectorHeaders if TADataCollectorHeader != self.dataTypeHeader}
        TADataResponseMsg = None
        if TADataRequestInformation:
            TADataRequestResponse = self.executeTAGetRequest(self.TADataRequestURL, TADataRequestInformation)
            TADataRequestStatus = TADataRequestResponse[0]
            if TADataRequestStatus:
                TADataResponseContainer = TADataRequestResponse[1].json()
                TADataResponseStatus = TADataResponseContainer[self.TAStatusHeader] == self.TAStatusSuccessName
                rawTADataResponseData = TADataResponseContainer[self.TADataHeader]
                if TADataResponseStatus:
                    sensorUnitInformation = rawTADataResponseData[self.TADataUnitsInformationHeader]
                    sensorUnits = {sensorID: sensorUnitData[self.TADataUnitHeader] for sensorID, sensorUnitData in sensorUnitInformation.items()}
                    sensorDescriptions = rawTADataResponseData[self.TADataDescriptionHeader]
                    print(sensorUnits)
                    print(sensorDescriptions)
                    userSetSensorLineColours = rawTADataResponseData[self.TADataColourHeader]
                    userSetSensorFactors = rawTADataResponseData[self.TADataFactorHeader]
                    sensorReadingsContainer = rawTADataResponseData[self.TADataSensorReadingsHeader]
                    for sensorReadings in sensorReadingsContainer:
                        sensorReadingTime = sensorReadings[self.TADataSensorReadingTimeHeader] if self.TADataSensorReadingTimeHeader in sensorReadings else None
                        if sensorReadingTime is not None:
                            sensorData = {sensorName: sensorValue for sensorName, sensorValue in sensorReadings.items() if sensorName != self.TADataSensorReadingTimeHeader}
                            for sensorID, sensorValue in sensorData.items():
                                sensorIDName = sensorDescriptions[sensorID] if sensorID in sensorDescriptions else None
                                sensorUnit = sensorUnits[sensorID] if sensorID in sensorUnits else None
                                TADataResponseDataCollector[self.dataMeasurementTime].append(sensorReadingTime)
                                TADataResponseDataCollector[self.dataSensorIDHeader].append(sensorID)
                                TADataResponseDataCollector[self.dataSensorNameHeader].append(sensorIDName)
                                TADataResponseDataCollector[self.dataValueHeader].append(sensorValue)
                                TADataResponseDataCollector[self.dataUnitHeader].append(sensorUnit)
                else:
                    TADataResponseMsg = rawTADataResponseData
            else:
                TADataResponseMsg = TADataRequestResponse[2]

        TADataResponseData = pd.DataFrame(TADataResponseDataCollector)
        TADataResponseData[self.dataTypeHeader] = TADataRequestInformation[self.TAModeFieldName].title()
        TADataResponseData[self.dataSensorIDHeader] = TADataResponseData[self.dataSensorIDHeader].apply(
            lambda sensorID: int(re.search("(\d+)", sensorID).group(1))
        )
        TADataResponseData[self.dataSensorNameHeader] = TADataResponseData[self.dataSensorNameHeader].apply(
            lambda sensorName: sensorName[re.search("\d+:", sensorName).span()[1]:].strip()
        )
        TADataResponseData = TADataResponseData.sort_values(by = [
            self.dataSensorIDHeader,
            self.dataMeasurementTime
        ])

        # print(TADataResponseData[self.dataSensorNameHeader].unique())
        print(TADataResponseData[self.dataSensorIDHeader].unique())

        return TADataResponseStatus, TADataResponseData, TADataResponseMsg

    def retrieveAnalogData(self, CMIName: str = None, profileName: None = str, fromDate: str = None, toDate: str = None):
        analogDataStatus = False
        analogData = []
        analogDataMsg = None

        analogRequestInformation = self.composeTADataRequest(CMIName, profileName, "analog", fromDate, toDate)
        analogRequestStatus = analogRequestInformation[0]
        if analogRequestStatus:
            analogDataRequest = analogRequestInformation[1]
            analogDataStatus, analogData, analogDataMsg = self.extractTADataResponseInformation(analogDataRequest)
        else:
            analogDataMsg = analogRequestInformation[2]

        return analogRequestStatus, 

    def retrieveDigitalData(self, CMIName: str = None, profileName: None = str, fromDate: str = None, toDate: str = None):
        digitalDataStatus = False
        digitalData = []
        digitalDataMsg = None

        digitalRequestInformation = self.composeTADataRequest(CMIName, profileName, "digital", fromDate, toDate)
        digitalRequestStatus = digitalRequestInformation[0]
        if digitalRequestStatus:
            digitalDataRequest = digitalRequestInformation[1]
            digitalDataStatus, digitalData, digitalDataMsg = self.extractTADataResponseInformation(digitalDataRequest)
        else:
            digitalDataMsg = digitalRequestInformation[2]

        return digitalDataStatus, digitalData, digitalDataMsg

    def executeTAGetRequest(self, url: str = None, params: list = [], keepSessionOpen: bool = False) -> (bool, list, str):
        TAGetRequestMsg = None
        TAGetRequestStatus = False
        TAGetRequestData = []
        if url and isinstance(url, str):
            if not self.TASession:
                self.setupSession()

            if self.TASession:
                TAGetRequestResponse = self.TASession.get(url, params = params, timeout = self.requestTimeoutTime)
                TAGetRequestStatus = TAGetRequestResponse.status_code == 200
                if TAGetRequestStatus:
                    TAGetRequestData = TAGetRequestResponse
                else:
                    TAGetRequestMsg = TAGetRequestResponse.text

        if not keepSessionOpen:
            self.closeSession()

        return TAGetRequestStatus, TAGetRequestData, TAGetRequestMsg

if __name__ == "__main__":
    DataRetrieverTA = DataRetrieverTA()