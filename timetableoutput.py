import pandas as pd
import os
from datetime import datetime, timedelta

basefolderinput = "C:/Users/ashok/Desktop/IIT RESEARCH/Task 4/eTPSS/Traction_Power_Supply_System_Modules/HSRIC_00_Projects/Case_2_P0.25B/Input_01_MTMM"
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
    for j in range(0, len(rows)-1):
        stationName = []
        stationNumber =[]
        distanceBetweenStations = []
        timeFromStarting = [df[2][rows[j]+1]]
        timeFromStarting_mins = []
        for k in range(rows[j]+4, rows[j+1]-1):
            stationName.append(df[1][k])
            stationNumber.append(df[2][k])
            if(k == rows[j]+4):
                continue
            else:
                distanceBetweenStations.append(abs(int(df[3][k])-int(df[3][k-1])))
            timeFromStarting_mins.append(int(df[4][k]))
        for i in range(0, len(timeFromStarting_mins)):
            values = df[2][rows[j]+1].split(":")
            h = int(timeFromStarting_mins[i]) // 60
            m = int(timeFromStarting_mins[i]) % 60
            timeFromStarting.append(str(timedelta(
                hours=h, minutes=m) + timedelta(hours=int(values[0]), minutes=int(values[1]))))
        for i in range(0, len(timeFromStarting_mins)):
            timeFromStarting_mins[i] = timeFromStarting_mins[i] + \
                int(datetime.strptime(df[2][rows[j]+1], "%H:%M").minute)
        temp = {"trainnumber": df[0][rows[j]+1], "startDistance": df[3][rows[j]+4],
                "trainType": df[6][rows[j]+1],
                "stationName": station_name,
                "stationNumber":stationNumber,
                "distanceBetweenStations": distanceBetweenStations,
                "timeFromStarting": timeFromStarting}
        final_dict.append(temp)
    for i in range(len(final_dict)):
        for j in station_numbers:
            if str(j) in final_dict[i]["stationNumber"]:
                continue
            else:
                final_dict[i]["stationNumber"].insert(j-1,str(j))
                final_dict[i]["timeFromStarting"].insert(j-1, "-")
    return final_dict

timeTableExcel(basefolderinput)