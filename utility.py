import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np


def timeTableData(basefolder):
    df = pd.read_csv(basefolder+"/TimeTableData.csv", header=None)
    rows = []
    final_dict = []
    timingGraph = []
    timingGraphInHrsAndMins = []
    for i in range(0, len(df)):
        if (df[0][i] == "TrainNumber "):
            rows.append(i)
    for j in range(0, len(rows)-1):
        stationName = []
        distanceFromStarting = []
        timeFromStarting = []
        dwelltime = []
        timeFromStarting_mins = []
        for k in range(rows[j]+4, rows[j+1]-1):
            stationName.append(df[1][k])
            distanceFromStarting.append(df[3][k])
            timeFromStarting_mins.append(int(df[4][k]))
            dwelltime.append(int(df[5][k]))
        dwell_counter = 0
        for i in range(0, len(dwelltime)):
            if (dwelltime[i] != 0):
                dwell_counter += 1
                stationName.insert(i+1, stationName[i])
                distanceFromStarting.insert(
                    2*i+1, distanceFromStarting[i+dwell_counter-1])
                timeFromStarting_mins.insert(
                    2*i+1, timeFromStarting_mins[i+dwell_counter-1]+dwelltime[i])
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
        temp = {"trainnumber": df[0][rows[j]+1], "startTime": df[2][rows[j]+1],
                "trainType": df[6][rows[j]+1],
                "stationName": stationName,
                "distanceFromStarting": distanceFromStarting,
                "timeFromStarting": timeFromStarting,
                "timeFromStartingInMins": timeFromStarting_mins,
                "dwelltime": dwelltime}
        final_dict.append(temp)
    splitDuration = (max(timingGraph) - min(timingGraph))//8
    timingGraph = [min(timingGraphInHrsAndMins)]
    timeToReplaceInMins = [0]
    values = timingGraph[0].split(":")
    for i in range(1, 9):
        timeToReplaceInMins.append(int(timeToReplaceInMins[i-1]+splitDuration))
        h = int(timeToReplaceInMins[i]//60)
        m = int(timeToReplaceInMins[i]) % 60
        timingGraph.append(str(timedelta(
            hours=h, minutes=m) + timedelta(hours=int(values[0]), minutes=int(values[1]))))
    dataToBeSent = {"calculativeData": final_dict,
                    "plottingData": [timingGraph, timeToReplaceInMins]}
    return dataToBeSent


def routeAltitudeData(basefolder):
    df2 = pd.read_csv(basefolder + "/RouteAltitudeData.csv")
    df3 = pd.read_csv(basefolder+"/AllStationData.csv")
    X_axis = df2["DistanceKM"]
    Y_axis = df2["HeightAboveGroundMSL"]
    plt.plot(X_axis, Y_axis, label='Route-Altitude graph')
    plt.xlabel("Distance From Source")
    plt.ylabel("Altitude")
    plt.xticks(df3["DistanceKMWithReferenceToStartingStation"],
               df3["StationName "])
    plt.legend()
    plt.show()


# basefolderoutput = "C:/Users/ashok/Desktop/IIT RESEARCH/SPIT_Interns_task/eTPSS/Traction_Power_Supply_System_Modules/HSRIC_00_Projects/Case_2_P0.25B/Case_2_P0.25B_Output"
# basefolderinput = "C:/Users/ashok/Desktop/IIT RESEARCH/SPIT_Interns_task/eTPSS/Traction_Power_Supply_System_Modules/HSRIC_00_Projects/Case_2_P0.25B/Input_01_MTMM"
# selected_trains = ["101"]


def TractiveEffortData(basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(basefolderoutput+"/TrainModuleOutput.csv")
    df_y = pd.read_csv(basefolderoutput+"/EffortOutput.csv")
    X_axis = []
    Y_axis = []
    for i in range(0, len(selected_trains)):
        if (int(df_x["Up/Downtrack_"+str(selected_trains[i])+"_0"]) == 0):
            partstr = "Uptrack"
        else:
            partstr = "Downtrack"
        Y_axis.append(df_y["TractiveEffort_"+partstr+"_" +
                      str(selected_trains[i])+"_0"])
        if (timeFlag == 1):
            X_axis = round(
                df_x["Time_"+partstr+"_"+str(selected_trains[i])+"_0"]*24*60)
            plt.xlabel("Time")
        else:
            X_axis = df_x["Distance_"+partstr+"_" +
                          str(selected_trains[i])+"_0"]*1000
            plt.xlabel("Distance")
    return X_axis, Y_axis


def BrakingEffortData(basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(basefolderoutput+"/TrainModuleOutput.csv")
    df_y = pd.read_csv(basefolderoutput+"/EffortOutput.csv")
    X_axis = []
    Y_axis = []
    for i in range(0, len(selected_trains)):
        if (int(df_x["Up/Downtrack_"+str(selected_trains[i])+"_0"]) == 0):
            partstr = "Uptrack"
        else:
            partstr = "Downtrack"
        Y_axis.append(df_y["BrakingEffort_"+partstr+"_" +
                      str(selected_trains[i])+"_0"])
        if (timeFlag == 1):
            X_axis = round(
                df_x["Time_"+partstr+"_"+str(selected_trains[i])+"_0"]*24*60)
            plt.xlabel("Time")
        else:
            X_axis = df_x["Distance_"+partstr+"_" +
                          str(selected_trains[i])+"_0"]*1000
            plt.xlabel("Distance")
    return X_axis, Y_axis


def ReactivePowerData(basefolderinput, basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(basefolderoutput+"/TrainModuleOutput.csv")
    df_p = pd.read_csv(basefolderinput+"/TrainElectricalData.csv", header=1)
    X_axis = pd.DataFrame()
    Y_axis = pd.DataFrame()
    inputdata = timeTableData(basefolderinput)
    for i in range(0, len(selected_trains)):
        if (int(df_x["Up/Downtrack_"+str(selected_trains[i])+"_0"]) == 0):
            partstr = "Uptrack"
        else:
            partstr = "Downtrack"
        for j in range(0, len(inputdata["calculativeData"])):
            if (inputdata["calculativeData"][j]["trainnumber"] == selected_trains[i]):
                t_type = inputdata["calculativeData"][j]["trainType"]
        result = df_p[str(t_type)][16]
        temp_y = df_x["ActivePower_"+partstr+"_"+str(selected_trains[i])+"_0"]
        Y_axis = temp_y*np.tan(np.arccos(result))
        if (timeFlag == 1):
            X_axis = round(
                df_x["Time_"+partstr+"_"+str(selected_trains[i])+"_0"]*24*60)
            plt.xlabel("Time")
        else:
            X_axis = df_x["Distance_"+partstr+"_" +
                          str(selected_trains[i])+"_0"]*1000
            plt.xlabel("Distance")
    print(X_axis, Y_axis)
    return X_axis, Y_axis


def ActivePowerData(basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(basefolderoutput+"/TrainModuleOutput.csv")
    X_axis = []
    Y_axis = []
    for i in range(0, len(selected_trains)):
        if (int(df_x["Up/Downtrack_"+str(selected_trains[i])+"_0"]) == 0):
            partstr = "Uptrack"
        else:
            partstr = "Downtrack"
        Y_axis.append(df_x["ActivePower_"+partstr+"_" +
                      str(selected_trains[i])+"_0"])
        if (timeFlag == 1):
            X_axis = round(
                df_x["Time_"+partstr+"_"+str(selected_trains[i])+"_0"]*24*60)
            plt.xlabel("Time")
        else:
            X_axis = df_x["Distance_"+partstr+"_" +
                          str(selected_trains[i])+"_0"]*1000
            plt.xlabel("Distance")
    return X_axis, Y_axis


def CurrentData(basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(basefolderoutput+"/TrainModuleOutput.csv")
    df_y = pd.read_csv(basefolderoutput+"/EffortOutput.csv")
    X_axis = []
    Y_axis = []
    for i in range(0, len(selected_trains)):
        if (int(df_x["Up/Downtrack_"+str(selected_trains[i])+"_0"]) == 0):
            partstr = "Uptrack"
        else:
            partstr = "Downtrack"
        Y_axis = df_y["TractiveEffort_"+partstr +
                      "_"+str(selected_trains[i])+"_0"]
        if (timeFlag == 1):
            X_axis = round(
                df_x["Time_"+partstr+"_"+str(selected_trains[i])+"_0"]*24*60*60)
        else:
            X_axis = df_x["Distance_"+partstr+"_" +
                          str(selected_trains[i])+"_0"]*1000
    plt.plot(X_axis, Y_axis)
    plt.show()


def VoltageData(basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(basefolderoutput+"/TrainModuleOutput.csv")
    df_y = pd.read_csv(basefolderoutput+"/EffortOutput.csv")
    X_axis = []
    Y_axis = []
    for i in range(0, len(selected_trains)):
        if (int(df_x["Up/Downtrack_"+str(selected_trains[i])+"_0"]) == 0):
            partstr = "Uptrack"
        else:
            partstr = "Downtrack"
        Y_axis = df_y["TractiveEffort_"+partstr +
                      "_"+str(selected_trains[i])+"_0"]
        if (timeFlag == 1):
            X_axis = round(
                df_x["Time_"+partstr+"_"+str(selected_trains[i])+"_0"]*24*60*60)
        else:
            X_axis = df_x["Distance_"+partstr+"_" +
                          str(selected_trains[i])+"_0"]*1000
    plt.plot(X_axis, Y_axis)
    plt.show()


def VelocityData(basefolderoutput, selected_trains, timeFlag):
    X_axis = []
    Y_axis = []
    df_x = pd.read_csv(basefolderoutput+"/TrainModuleOutput.csv")
    for i in range(0, len(selected_trains)):
        if (int(df_x["Up/Downtrack_"+str(selected_trains[i])+"_0"]) == 0):
            partstr = "Uptrack"
        else:
            partstr = "Downtrack"
        Y_axis.append(df_x["Velocity_"+partstr+"_" +
                      str(selected_trains[i])+"_0"])
        if (timeFlag == 1):
            X_axis = round(
                df_x["Time_"+partstr+"_"+str(selected_trains[i])+"_0"]*24*60)
            plt.xlabel("Time")
        else:
            X_axis = df_x["Distance_"+partstr+"_" +
                          str(selected_trains[i])+"_0"]*1000
            plt.xlabel("Distance")
    return X_axis, Y_axis

# timeTableData(basefolderinput)
