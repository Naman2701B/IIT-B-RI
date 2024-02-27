import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import mplcursors
from scipy import io


def timeTableData(basefolderinput):
    df = pd.read_csv(basefolderinput+"/TimeTableData.csv", header=None)
    df2 = pd.read_csv(basefolderinput+"/AllStationData.csv")
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
        distanceFromStarting = []
        timeFromStarting = []
        timeFromStarting_mins = []
        for k in range(rows[j]+4, rows[j+1]-1):
            stationName.append(df[1][k])
            distanceFromStarting.append(df[3][k])
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
            distanceGraph.append(int(distanceFromStarting[i]))
        temp = {"trainnumber": df[0][rows[j]+1], "startTime": df[2][rows[j]+1], "endDistance": df[3][rows[j]+len(stationName)+3], "startDistance": df[3][rows[j]+4],
                "trainType": df[6][rows[j]+1],
                "stationName": stationName,
                "distanceFromStarting": distanceFromStarting,
                "timeFromStarting": timeFromStarting,
                "timeFromStartingInMins": timeFromStarting_mins}
        final_dict.append(temp)
    splitDuration = (max(timingGraph) - min(timingGraph))//8
    splitDistance = (max(distanceGraph)-min(distanceGraph))//5
    timingGraph = [min(timingGraphInHrsAndMins)]
    distanceToReplace = df2["DistanceKMWithReferenceToStartingStation"].to_list(
    )
    distanceGraph = [min(distanceGraph)]
    timeToReplaceInMins = [0]
    values = timingGraph[0].split(":")
    for i in range(1, 9):
        timeToReplaceInMins.append(int(timeToReplaceInMins[i-1]+splitDuration))
        h = int(timeToReplaceInMins[i]//60)
        m = int(timeToReplaceInMins[i]) % 60
        timingGraph.append(str(timedelta(
            hours=h, minutes=m) + timedelta(hours=int(values[0]), minutes=int(values[1]))))
    for i in range(1, 6):
        distanceGraph.append(distanceGraph[i-1]+splitDistance)
    dataToBeSent = {"calculativeData": final_dict,
                    "plottingData": [timingGraph, timeToReplaceInMins, distanceGraph, distanceToReplace]}
    return dataToBeSent


def routeAltitudeData(basefolder):
    df2 = pd.read_csv(basefolder + "/RouteAltitudeData.csv")
    df3 = pd.read_csv(basefolder + "/AllStationData.csv")
    X_axis = df2["DistanceKM"]
    Y_axis = df2["HeightAboveGroundMSL"]
    markers_onx = []
    markers_ony = []
    station_names = []
    for i in range(0, len(df3["DistanceKMWithReferenceToStartingStation"])):
        markers_onx.append(df3["DistanceKMWithReferenceToStartingStation"][i])
        station_names.append(df3["StationName "][i])
    for i in range(0, len(X_axis)):
        if X_axis[i] in markers_onx:
            markers_ony.append(Y_axis[i])
    plt.scatter(markers_onx, markers_ony)
    for i, txt in enumerate(station_names):
        plt.annotate(
            txt, (markers_onx[i], markers_ony[i]), horizontalalignment='center')
    plt.plot(X_axis, Y_axis, label='Route-Altitude graph')
    plt.xlabel("Stations")
    plt.ylabel("Altitude(M)")
    plt.legend()
    plt.grid(alpha=0.3)
    cursor = mplcursors.cursor(hover=True)
    plt.show()


def TractiveEffortData(basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(basefolderoutput+"/TrainModuleOutput.csv")
    df_y = pd.read_csv(basefolderoutput+"/EffortOutput.csv")
    X_axis = []
    Y_axis = []
    if (int(df_x["Up/Downtrack_"+str(selected_trains)+"_0"][0]) == 0):
        partstr = "Uptrack"
    else:
        partstr = "Downtrack"
    Y_axis.append(df_y["TractiveEffort_"+partstr+"_" +
                       str(selected_trains)+"_0"])
    if (timeFlag == 1):
        X_axis.append(round(
            df_x["Time_"+partstr+"_"+str(selected_trains)+"_0"]*60))
    else:
        X_axis.append(df_x["Distance_"+partstr+"_" +
                           str(selected_trains)+"_0"])
    return X_axis, Y_axis


def BrakingEffortData(basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(basefolderoutput+"/TrainModuleOutput.csv")
    df_y = pd.read_csv(basefolderoutput+"/EffortOutput.csv")
    X_axis = []
    Y_axis = []
    if (int(df_x["Up/Downtrack_"+str(selected_trains)+"_0"][0]) == 0):
        partstr = "Uptrack"
    else:
        partstr = "Downtrack"
    Y_axis.append(df_y["BrakingEffort_"+partstr+"_" +
                       str(selected_trains)+"_0"])
    if (timeFlag == 1):
        X_axis.append(round(
            df_x["Time_"+partstr+"_"+str(selected_trains)+"_0"]*60))
    else:
        X_axis.append(df_x["Distance_"+partstr+"_" +
                           str(selected_trains)+"_0"])
    return X_axis, Y_axis


def ReactivePowerData(basefolderinput, basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(basefolderoutput+"/TrainModuleOutput.csv")
    df_p = pd.read_csv(basefolderinput+"/TrainElectricalData.csv", header=1)
    X_axis = []
    Y_axis = []
    inputdata = timeTableData(basefolderinput)
    for j in range(0, len(inputdata["calculativeData"])):
        if (inputdata["calculativeData"][j]["trainnumber"] == selected_trains):
            t_type = inputdata["calculativeData"][j]["trainType"]
    if (int(df_x["Up/Downtrack_"+str(selected_trains)+"_0"][0]) == 0):
        partstr = "Uptrack"
    else:
        partstr = "Downtrack"
    result = df_p[str(t_type)][16]
    temp_y = df_x["ActivePower_"+partstr+"_"+str(selected_trains)+"_0"]
    Y_axis.append(temp_y*np.tan(np.arccos(result)))
    if (timeFlag == 1):
        X_axis.append(round(
            df_x["Time_"+partstr+"_"+str(selected_trains)+"_0"]*60))
    else:
        X_axis.append(df_x["Distance_"+partstr+"_" +
                           str(selected_trains)+"_0"])
    return X_axis, Y_axis


def ActivePowerData(basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(basefolderoutput+"/TrainModuleOutput.csv")
    X_axis = []
    Y_axis = []
    if (int(df_x["Up/Downtrack_"+str(selected_trains)+"_0"][0]) == 0):
        partstr = "Uptrack"
    else:
        partstr = "Downtrack"
    Y_axis.append(df_x["ActivePower_"+partstr+"_" +
                       str(selected_trains)+"_0"])
    if (timeFlag == 1):
        X_axis.append(round(
            df_x["Time_"+partstr+"_"+str(selected_trains)+"_0"]*60))
    else:
        X_axis.append(df_x["Distance_"+partstr+"_" +
                           str(selected_trains)+"_0"])
    return X_axis, Y_axis


def CurrentData(basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(basefolderoutput+"/TrainModuleOutput.csv")
    df_y = pd.read_csv(basefolderoutput+"/EffortOutput.csv")
    X_axis = []
    Y_axis = []
    if (int(df_x["Up/Downtrack_"+str(selected_trains)+"_0"][0]) == 0):
        partstr = "Uptrack"
    else:
        partstr = "Downtrack"
    Y_axis.append(df_y["TractiveEffort_"+partstr +
                       "_"+str(selected_trains)+"_0"])
    if (timeFlag == 1):
        X_axis.append(round(
            df_x["Time_"+partstr+"_"+str(selected_trains)+"_0"]*60*60))
    else:
        X_axis.append(df_x["Distance_"+partstr+"_" +
                           str(selected_trains)+"_0"])
    plt.plot(X_axis, Y_axis)
    plt.show()


def VoltageData(basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(basefolderoutput+"/TrainModuleOutput.csv")
    df_y = pd.read_csv(basefolderoutput+"/EffortOutput.csv")
    X_axis = []
    Y_axis = []
    if (int(df_x["Up/Downtrack_"+str(selected_trains)+"_0"][0]) == 0):
        partstr = "Uptrack"
    else:
        partstr = "Downtrack"
    Y_axis = df_y["TractiveEffort_"+partstr +
                  "_"+str(selected_trains)+"_0"]
    if (timeFlag == 1):
        X_axis.append(round(
            df_x["Time_"+partstr+"_"+str(selected_trains)+"_0"]*60*60))
    else:
        X_axis.append(df_x["Distance_"+partstr+"_" +
                           str(selected_trains)+"_0"])
    plt.plot(X_axis, Y_axis)
    plt.show()


def VelocityData(basefolderoutput, selected_trains, timeFlag):
    X_axis = []
    Y_axis = []
    df_x = pd.read_csv(basefolderoutput+"/TrainModuleOutput.csv")
    if (int(df_x["Up/Downtrack_"+str(selected_trains)+"_0"][0]) == 0):
        partstr = "Uptrack"
    else:
        partstr = "Downtrack"
    Y_axis.append(df_x["Velocity_"+partstr+"_" +
                       str(selected_trains)+"_0"])
    if (timeFlag == 1):
        X_axis.append(round(
            df_x["Time_"+partstr+"_"+str(selected_trains)+"_0"]*60))
    else:
        X_axis.append(df_x["Distance_"+partstr+"_" +
                           str(selected_trains)+"_0"])
    return X_axis, Y_axis


outputfolder = "C:/Users/ashok/Desktop/etpss/OLFA_213159_20-07-2023_R"


def loadFlowAnalysis(outputfolder):
    file = io.loadmat(file_name=outputfolder+"/data_ntwrk.mat")
    print(file)


loadFlowAnalysis(outputfolder)
