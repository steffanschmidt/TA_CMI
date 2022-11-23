#!/usr/bin/env python3
import datetime as dt

class BaseWorkerTA:

    def __init__(self):
        # Base Information
        self.defaultRequestDays = 1
        self.dateFormat = "%Y-%m-%d"
        self.TADateTimeRequestFormat = f"{self.dateFormat} %H:%M:%S"

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

    def processDateRange(self, fromDate: dt.datetime = None, toDate: dt.datetime = None) -> (str, str):
        processedFromDate = None
        processedToDate = None

        if fromDate and toDate:
            processedFromDate = fromDate
            processedToDate = toDate
        if not fromDate and not toDate:
            processedToDate = dt.datetime.now().replace(microsecond = 0)
            processedFromDate = processedToDate - dt.timedelta(days = self.defaultRequestDays)
        elif not fromDate:
            processedToDate = self.convertStringToDateTime(processedToDate)
            processedFromDate = processedToDate - dt.timedelta(days = self.defaultRequestDays) if toDate else None
        elif not toDate:
            processedToDate = dt.datetime.now()

        processedFromDate = self.convertDateTimeToString(processedFromDate)
        processedToDate = self.convertDateTimeToString(processedToDate)
        return processedFromDate, processedToDate

    """

    """
    def convertDateTimeToString(self, dateTime: dt.datetime = None) -> str:
        dateTimeString = None
        if isinstance(dateTime, (dt.date, dt.datetime)):
            try:
                dateTimeString = dt.datetime.strftime(dateTime, self.TADateTimeRequestFormat)
            except:
                dateTimeString = None
        elif isinstance(dateTime, str):
            dateTimeString = dateTime
    
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