"""

This Python script processes railway timetable data and generates a structured output with various details for each train.

Dependencies:
- pandas: Used for data manipulation and reading CSV files.
- os: Used for file path manipulations.
- datetime: Used for handling time-related data.

Functions:
    timeTableExcel(basefolderinput)
        Processes timetable data from CSV files and generates a structured dictionary containing train details,
        including train number, station names, distances between stations, dwell times, and departure times.

        Parameters:
        - basefolderinput (str): The base folder path where the input CSV files (TimeTableData.csv and AllStationData.csv) are located.

        Returns:
        - final_dict (list of dict): A list of dictionaries, each containing the following keys:
            - trainnumber (str): The train number.
            - startDistance (str): The starting distance of the train route.
            - trainType (str): The type of the train.
            - stationNameToDisplay (list of str): A list of all station names to display.
            - stationNumber (list of str): A list of station numbers.
            - distanceBetweenStations (list of int): Distances between consecutive stations.
            - dwellTime (list of str): The dwell time at each station.
            - timeFromStarting (list of str): Times from the starting station.
            - actualStationName (list of str): Names of the actual stations on the route.
            - departureTime (list of str): Departure times from each station.

Example Usage:
    # Assuming the input files are located in the specified directory
    basefolderinput = "/path/to/input/files"
    result = timeTableExcel(basefolderinput)

    # The result is a list of dictionaries with train timetable details
    for train in result:
        print(train)
"""

import pandas as pd
import os
from datetime import datetime, timedelta

def timeTableExcel(basefolderinput):
    df = pd.read_csv(os.path.join(basefolderinput,"TimeTableData.csv"), header=None)
    df2 = pd.read_csv(os.path.join(basefolderinput,"AllStationData.csv"))
    station_numbers = df2["StationNumber "]
    station_name= df2["StationName "].to_list()
    rows = []
    final_dict = []
    for i in range(0, len(df)):
        if (df[0][i] == "TrainNumber "):
            rows.append(i)
    rows.append(len(df)+1)    
    for j in range(1, len(rows)):
        stationName = []
        stationNumber =[]
        dwellTime = []
        distanceBetweenStations = []
        timeFromStarting = [df[2][rows[j-1]+1]]
        timeFromStarting_mins = []
        values = df[2][rows[j-1]+1].split(":")
        for k in range(rows[j-1]+4, rows[j]-1):
            stationName.append(df[1][k])
            stationNumber.append(df[2][k])
            dwellTime.append(df[5][k])
            if(k == rows[j-1]+4):
                continue
            else:
                distanceBetweenStations.append(abs(int(df[3][k])-int(df[3][k-1])))
            timeFromStarting_mins.append(int(df[4][k]))
        temp = str(timedelta(hours=int(values[0]), minutes=int(values[1]))+timedelta(hours=(int(dwellTime[0])//60), minutes=(int(dwellTime[0])%60)))
        departureTime = [temp]
        for i in range(0, len(timeFromStarting_mins)):
            h = int(timeFromStarting_mins[i]) // 60
            m = int(timeFromStarting_mins[i]) % 60
            timeFromStarting.append(str(timedelta(
                hours=h, minutes=m) + timedelta(hours=int(values[0]), minutes=int(values[1]))))
            departureTime.append(str(timedelta(
                hours=h, minutes=m) +timedelta(hours=int(values[0]), minutes=int(values[1]))+timedelta(hours=(int(dwellTime[i-1])//60), minutes=(int(dwellTime[i-1])%60))))
        for i in range(0, len(timeFromStarting_mins)):
            timeFromStarting_mins[i] = timeFromStarting_mins[i] + int(datetime.strptime(df[2][rows[j-1]+1], "%H:%M").minute)
        temp = {"trainnumber": df[0][rows[j-1]+1], "startDistance": df[3][rows[j-1]+4],
                "trainType": df[6][rows[j-1]+1],
                "stationNameToDisplay": station_name,
                "stationNumber":stationNumber,
                "distanceBetweenStations": distanceBetweenStations,
                "dwellTime": dwellTime,
                "timeFromStarting": timeFromStarting, "actualStationName": stationName, "departureTime": departureTime}
        final_dict.append(temp)
    for i in range(len(final_dict)):
        for j in station_numbers:
            if str(j) in final_dict[i]["stationNumber"]:
                continue
            else:
                final_dict[i]["stationNumber"].insert(j-1,str(j))
                final_dict[i]["timeFromStarting"].insert(j-1, "-")
                final_dict[i]["dwellTime"].insert(j-1,"-")
                final_dict[i]["departureTime"].insert(j-1,"-")
    return final_dict