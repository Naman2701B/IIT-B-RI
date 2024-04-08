import pandas as pd
import os
from datetime import datetime, timedelta

# basefolderinput = "C:/Users/ashok/Desktop/IIT RESEARCH/Task 4/eTPSS/Traction_Power_Supply_System_Modules/HSRIC_00_Projects/Case_2_P0.25B/Input_01_MTMM"
def timeTableExcel(basefolderinput):
    df = pd.read_csv(os.path.join(basefolderinput,"TimeTableData.csv"), header=None)
    df2 = pd.read_csv(os.path.join(basefolderinput,"AllStationData.csv"))
    rows = []
    final_dict = []
    timingGraph = []
    distanceGraph = []
    timingGraphInHrsAndMins = []
    for i in range(0, len(df)):
        if (df[0][i] == "TrainNumber "):
            rows.append(i)
    for j in range(0, len(rows)-1):
        stationName = []
        stationNumber =[]
        distanceBetweenStations = []
        timeFromStarting = []
        timeFromStarting_mins = []
        for k in range(rows[j]+4, rows[j+1]-1):
            stationName.append(df[1][k])
            stationNumber.append(df[2][k])
            if(k == rows[j]+4):
                continue
            else:
                distanceBetweenStations.append(int(df[3][k])-int(df[3][k-1]))
            timeFromStarting_mins.append(int(df[4][k]))
        for i in range(0, len(timeFromStarting_mins)):
            values = df[2][rows[j]+1].split(":")
            h = int(timeFromStarting_mins[i]) // 60
            m = int(timeFromStarting_mins[i]) % 60
            timeFromStarting.append(str(timedelta(
                hours=h, minutes=m) + timedelta(hours=int(values[0]), minutes=int(values[1]))))
            timingGraphInHrsAndMins.append(timeFromStarting[i])
        for i in range(0, len(timeFromStarting_mins)):
            timeFromStarting_mins[i] = timeFromStarting_mins[i] + \
                int(datetime.strptime(df[2][rows[j]+1], "%H:%M").minute)
            timingGraph.append(timeFromStarting_mins[i])
            distanceGraph.append(int(distanceBetweenStations[i]))
        temp = {"trainnumber": df[0][rows[j]+1], "startTime": df[2][rows[j]+1], "startDistance": df[3][rows[j]+4],
                "trainType": df[6][rows[j]+1],
                "stationName": stationName,
                "stationNumber":stationNumber,
                "distanceBetweenStations": distanceBetweenStations,
                "timeFromStarting": timeFromStarting}
        final_dict.append(temp)
    # print(final_dict)
    return final_dict

# timeTableExcel(basefolderinput)